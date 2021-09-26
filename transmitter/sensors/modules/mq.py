
# adapted from sandboxelectronics.com/?p=165

import time
import math

from requests import check_compatibility
from transmitter.sensors.modules.MCP3008 import MCP3008
from observers.observable import Observable, Observer

class MQ(Observable):

    MQ_PIN                       = 0        # define which analog input channel you are going to use (MCP3008)
    ######################### Hardware Related Macros #########################
    MAX_MILI_VOLTAGE             = 2048.0
    RL_VALUE                     = 5        # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 9.83     # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from the chart in datasheet
 
    ######################### Software Related Macros #########################
    CALIBARAION_SAMPLE_TIMES     = 10       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 500      # define the time interval(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define the time interval(in milisecond) between each samples in
    READ_SAMPLE_TIMES            = 5        # define how many samples you are going to take in normal operation 
                                            # normal operation
 
    ######################### Application Related Macros ######################
    GAS_LPG                      = 0
    GAS_CO                       = 1
    GAS_SMOKE                    = 2

    def __init__(self, Ro=10, analogPin=0, observers: Observable=None):
        Observable.__init__(self, observers)
        self.Ro = Ro
        self.MQ_PIN = analogPin
        self.adc = MCP3008(bus=0, device=0)
        
        # CALIBRATE 3RD PARAMETER
        self.LPGCurve = [2.3+3.0,0.21,-0.41]    # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent"
                                            # to the original curve. 
                                            # data format:{ x, y, slope}; point1: (lg200, 0.21), point2: (lg10000, -0.59) 
        self.COCurve = [2.3+3.0,0.72,-0.32]     # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg200, 0.72), point2: (lg10000,  0.15)
        self.SmokeCurve =[2.3+3.0,0.53,-0.64]   # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg200, 0.53), point2: (lg10000,  -0.22)  
                
        self.notify_observers("MQ: Calibrating MQ-2 sensor...")
        self.Ro = self.MQCalibration(self.MQ_PIN)
        self.notify_observers("MQ: Calibration is done...")
        self.notify_observers("MQ: Ro=%f kohm" % self.Ro)
    
    def MQPercentage(self):
        val = {}
        read = self.MQRead(self.MQ_PIN)
        val["LPG"]  = self.MQGetGasPercentage(read/self.Ro, self.GAS_LPG)
        val["CO"]   = self.MQGetGasPercentage(read/self.Ro, self.GAS_CO)
        val["CO2"]  = self.MQGetGasPercentage(read/self.Ro, self.GAS_SMOKE)
        return val
        
    ######################### MQResistanceCalculation #########################
    # Input:   raw_adc - raw value read from adc, which represents the voltage
    # Output:  the calculated sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 
    def MQResistanceCalculation(self, raw_adc):
        return float(self.RL_VALUE*(self.MAX_MILI_VOLTAGE-raw_adc)/float(raw_adc))
     
     
    ######################### MQCalibration ####################################
    # Input:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          MQResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
    #          10, which differs slightly between different sensors.
    ############################################################################ 
    def MQCalibration(self, mq_pin):
        val = 0.0
        for i in range(self.CALIBARAION_SAMPLE_TIMES):          # take multiple samples
            raw_adc = self.adc.read(mq_pin)
            val += self.MQResistanceCalculation(raw_adc)
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            self.MQPrintCalibrationPercentage(i)

        val = val/self.CALIBARAION_SAMPLE_TIMES                 # calculate the average value

        val = val/self.RO_CLEAN_AIR_FACTOR                      # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                # according to the chart in the datasheet 
        return val
      
    def MQPrintCalibrationPercentage(self, progress):
        if progress % (self.CALIBARAION_SAMPLE_TIMES / 5) == 0:
            self.notify_observers(f"MQ: Calibrating: {str((progress+1)/self.CALIBARAION_SAMPLE_TIMES*100.0)}% done.")

    #########################  MQRead ##########################################
    # Input:   mq_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target
    #          gas. The sample times and the time interval between samples could be configured
    #          by changing the definition of the macros.
    ############################################################################ 
    def MQRead(self, mq_pin):
        rs = 0.0

        for i in range(self.READ_SAMPLE_TIMES):
            raw_adc = self.adc.read(mq_pin)
            rs += self.MQResistanceCalculation(raw_adc)
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)

        rs /= self.READ_SAMPLE_TIMES

        return rs
     
    #########################  MQGetGasPercentage ##############################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function passes different curves to the MQGetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 
    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        if ( gas_id == self.GAS_LPG ):
            return self.MQGetPercentage(rs_ro_ratio, self.LPGCurve)
        elif ( gas_id == self.GAS_CO ):
            return self.MQGetPercentage(rs_ro_ratio, self.COCurve)
        elif ( gas_id == self.GAS_SMOKE ):
            return self.MQGetPercentage(rs_ro_ratio, self.SmokeCurve)
        return 0
     
    #########################  MQGetPercentage #################################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
    #          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
    #          value.
    ############################################################################ 
    def MQGetPercentage(self, rs_ro_ratio, pcurve):
        if rs_ro_ratio < 0:
            rs_ro_ratio = 0
        power = ((math.log(rs_ro_ratio) - pcurve[1]) / pcurve[2]) + pcurve[0]
        ans = (math.pow(10, power))
        return ans
