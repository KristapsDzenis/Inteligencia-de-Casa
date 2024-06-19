import paho.mqtt.client as mqtt
import secrets
import random
import time
from datetime import date, datetime
import json

# define client
client = mqtt.Client("Biometric door lock")

# connect to the broker on an appropriate port
client.connect("broker.hivemq.com", 1883)


while True:
    fingerprint = secrets.token_hex(16)
    lock_action = random.choice(["locked","unlocked"])

    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y.%m.%d %H.%M.%S")

    data = [str(fingerprint), str(lock_action), str(timestamp)]

    data_encoded = json.dumps(data)

    day = date.today()  # date function call
    clock = datetime.now()  # time function calls
    time_time = datetime.time(clock)

    client.publish("smarthouse/doorlock/data", data_encoded)

    print("Just published: date-" + str(day) + " time-" + str(time_time) + "; data: " + data_encoded + " to topic: 'smarthouse/doorlock/data'")

    num = random.randint(3, 10)
    time.sleep(num)

