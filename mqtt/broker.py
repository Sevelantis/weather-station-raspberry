import paho.mqtt.client as mqtt

class Broker:
    def __init__(self):
        self.broker='mqtt' # ip
        self.port=1883
        
    
    def on_publish(self, client, data, result): # callback
        print('data published')
    
    # --todo turn into sed
    # '  # urls = ["http://127.0.0.1:8086"]' -> '  urls = ["http://influxdb:8086"]'
    # '  # database = "telegraf"' -> '  database = "sensors"'
    # '  # skip_database_creation = false' -> '  skip_database_creation = true'
    # '  # username = "telegraf"' -> '  username = "telegraf"'
    # '  # password = "metricsmetricsmetricsmetrics"' -> '  password = "telegraf123"'
    # '#   servers = ["tcp://127.0.0.1:1883"]' -> '  servers = ["tcp://mqtt:1883"]'
    # '#   data_format = "influx"' -> '  data_format = "influx"'
