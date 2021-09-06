# weather-station

### Project explanation:
  - Raspberry Pi 4, 2GB RAM, OS: Linux Raspbian OS Lite
  - Some external sensors (DHT11, BMP280, DS18B20, HC-SR04, MQ-2)
  - Docker containers
 
### Stack:
  - Docker creates containers:
    - MQTT
    - InfluxDB
    - Node-Exporter
    - Prometheus
    - Grafana
  - Python object-oriented app collects real-time sensor data'
  - Transmitter(the app) publishes collected data through the MQTT server
  - Receiver catches published data through the same MQTT server and sends it to InfluxDB
  - Grafana has two data sources added:
    - Influxdb - sensors data
    - Prometheus - host metrics
  - Grafana is the endpoint of the stack and has some dashboard created in order to visualise the data

## Sensors Dashboard:
![Alt text](/readme-files/diagnostics-grafana-timelapse.gif?raw=true "Grafana dashboard timelapse chart - sensors.")
## Host Metrics Dashboard:
![Alt text](/readme-files/sensors-grafana-timelapse.gif?raw=true "Grafana dashboard timelapse chart - Raspberry Pi Diagnostic info")
