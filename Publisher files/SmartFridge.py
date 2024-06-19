import paho.mqtt.client as paho
import time
import random
import json
from datetime import datetime 

try:
    def on_publish(client, userdata, mid):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Published to SmartFridge at ->", current_time)  


    client = paho.Client()
    client.on_publish = on_publish
    client.connect('broker.hivemq.com', 1883)
    client.loop_start()




    while True:
        humidity = random.randint(0, 100)
        DoorStatus = random.choice([True, False])
        Temperature = random.randint(-6, 0)
        fridgeid = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data = [humidity, DoorStatus, Temperature, fridgeid]
        data_encoded = json.dumps(data)
        client.publish("smarthouse/fridge/data", data_encoded)
        time.sleep(7)
except:
    print("ConnectionRefusedError or JSONEncodeError")
