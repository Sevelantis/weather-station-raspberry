import paho.mqtt.client as paho

class Broker:
    def __init__(self):
        self.broker='mqtt' # ip
        self.port=1883
        
    
    def on_publish(self, client, data, result): # callback
        print('data published')
    
