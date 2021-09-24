import math
from .lib import i2c
import RPi.GPIO as GPIO
import smbus2
from time import *
from observers.observable import Observable

class HMC5883L(Observable):
	
	configuration_reg_A 		= 0x00
	configuration_reg_B 		= 0x01
	mode_reg 				= 0x02
	axis_x_data_register_MSB 	= 0x03
	axis_x_data_register_LSB 		= 0x04
	axis_z_data_register_MSB 		= 0x05
	axis_z_data_register_LSB 		= 0x06
	axis_y_data_register_MSB 		= 0x07
	axis_y_data_register_LSB 		= 0x08
	status_reg 				= 0x09
	identification_reg_A 	= 0x10
	identification_reg_B 	= 0x11
	identification_reg_C 	= 0x12
	measurement_continuous 		= 0x00
	measurement_single_shot 	= 0x01
	measurement_idle 		= 0x03
	
	def __init__(self, port=0, addr=0x1e, gauss=1.3, observers = []):
		Observable.__init__(self, observers=observers)
		
		self.bus = i2c.i2c(port, addr)
		self.set_scale(gauss)
		self.set_continuous_mode()
		self.set_declination(2, 15)
		self.notify_observers(f'HMC5883L: Init Device.')
		
	def close(self) -> None:
		self.remove_option(self.mode_reg, self.measurement_continuous)
		self.set_option(self.mode_reg, self.measurement_idle)
		self.bus.close()

	def set_continuous_mode(self):
		self.set_option(self.mode_reg, self.measurement_continuous)
		
	def set_scale(self, gauss):
		if gauss == 0.88:
			self.scale_reg = 0x00
			self.scale = 0.73
		elif gauss == 1.3:
			self.scale_reg = 0x01
			self.scale = 0.92
		elif gauss == 1.9:
			self.scale_reg = 0x02
			self.scale = 1.22
		elif gauss == 2.5:
			self.scale_reg = 0x03
			self.scale = 1.52
		elif gauss == 4.0:
			self.scale_reg = 0x04
			self.scale = 2.27
		elif gauss == 4.7:
			self.scale_reg = 0x05
			self.scale = 2.56
		elif gauss == 5.6:
			self.scale_reg = 0x06
			self.scale = 3.03
		elif gauss == 8.1:
			self.scale_reg = 0x07
			self.scale = 4.35
		
		self.scale_reg = self.scale_reg << 5
		self.set_option(self.configuration_reg_B, self.scale_reg)
		
	def set_declination(self, degree, min = 0):
		self.declinationDeg = degree
		self.declinationMin = min
		self.declination = (degree+min/60) * (math.pi/180)
		
	def set_option(self, register, *function_set):
		options = 0x00
		for function in function_set:
			options = options | function
		self.bus.write_byte(register, options)
		
	# Adds to existing options of register	
	def add_option(self, register, *function_set):
		options = self.bus.read_byte(register)
		for function in function_set:
			options = options | function
		self.bus.write_byte(register, options)
		
	# Removes options of register	
	def remove_option(self, register, *function_set):
		options = self.bus.read_byte(register)
		for function in function_set:
			options = options & (function ^ 0b11111111)
		self.bus.write_byte(register, options)
		
	def get_declination(self):
		return (self.declinationDeg, self.declinationMin)
	
	def get_declination_str(self):
		return str(self.declinationDeg)+"\u00b0 "+str(self.declinationMin)+"'"
	
	# Returns heading in degrees and minutes
	def get_heading(self):
		(scaled_x, scaled_y, scaled_z) = self.get_axes()
		headingRad = math.atan2(scaled_y, scaled_x)
		headingRad += self.declination

		# Correct for reversed heading
		if(headingRad < 0):
			headingRad += 2*math.pi
			
		# Check for wrap and compensate
		if(headingRad > 2*math.pi):
			headingRad -= 2*math.pi
			
		# Convert to degrees from radians
		headingDeg = headingRad * 180/math.pi
		degrees = math.floor(headingDeg)
		minutes = round(((headingDeg - degrees) * 60))
		return (degrees, minutes)
	
	def get_heading_str(self):
		(degrees, minutes) = self.get_heading()
		return str(degrees)+"\u00b0 "+str(minutes)+"'"
		
	def get_axes(self):
		read = self.bus.read_3s16int(self.axis_x_data_register_MSB)
		if not read:
		 	return (0,0,0)
		(magno_x, magno_z, magno_y) = read

		if (magno_x == -4096):
			magno_x = None
		else:
			magno_x = round(magno_x * self.scale, 4)
			
		if (magno_y == -4096):
			magno_y = None
		else:
			magno_y = round(magno_y * self.scale, 4)
			
		if (magno_z == -4096):
			magno_z = None
		else:
			magno_z = round(magno_z * self.scale, 4)
			
		return (magno_x, magno_y, magno_z)
		