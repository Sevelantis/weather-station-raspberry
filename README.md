# weather-station

### Project brief:
  - Raspberry Pi 4, 2GB RAM, OS: Linux Raspbian OS Lite
  - Some external sensors (DHT11, BMP280, DS18B20, HC-SR04, MQ-2, HMC5883L)
  - Docker
  - Python
  - Grafana's internal alerting system - SMTP/mail
 
### Techstack:
  - Docker containers:
    - MQTT
    - InfluxDB
    - Node-Exporter
    - Prometheus
    - Grafana
  - Python object-oriented app collects real-time sensor data'
  - Transmitter(the app) publishes collected data using the MQTT server
  - Receiver catches published data using the same MQTT server, the receiver sends it to InfluxDB container
  - Grafana:
      - Data sources:
        - Influxdb - sensors data
        - Prometheus - host metrics
      - Dashboards:
        - sensors (data from hygrometer, thermometer, barometer, gas sensor and ultrasonic length sensor)
        - diagnostics (hardware info, CPU temp, CPU load, RAM usage, Disk/Network I/O, and more...)
      - Alerts:
        - via email - Grafana's internal alerting system using the gmail's SMTP server
  - Grafana is the endpoint of the stack and has some dashboards created in order to visualise received data:

### RPi automation:
Start application on every RPi boot  
```
@reboot /home/pi/weather-station/start.sh
30 */3 * * * /home/pi/weather-station/start.sh -r

```

## Gas sensor Dashboard
![Alt text](/readme-files/gas-sensor-grafana-timelapse.gif?raw=true "CH4 / CO / CO2")
## Other sensors Dashboard:
![Alt text](/readme-files/diagnostics-grafana-timelapse.gif?raw=true "Grafana dashboard timelapse chart - sensors.")
## Host Metrics Dashboard:
![Alt text](/readme-files/sensors-grafana-timelapse.gif?raw=true "Grafana dashboard timelapse chart - Raspberry Pi Diagnostic info")
