import time
import paho.mqtt.client as mqtt
import random
import json
from datetime import datetime, date

# I have assigned for the broker,topic and port a variable; so I do not need to type them each time.

MQTT_Broker = "broker.hivemq.com"
MQTT_Port = 1883
MQTT_Topic = "smarthouse/sensors/motion"

# Added a location dictionary for the house creating a unique ID for each motion sensor.
location_map = {
    0: "Gate",
    1: "First Bedroom",
    2: "Second Bedroom",
    3: "Third Bedroom",
    4: "Forth Bedroom",
    5: "Upstairs Corridor",
    6: "Kitchen",
    7: "Dining Room",
    8: "Living Room",
    9: "Study Room",
    10: "Entrance"
}

client = mqtt.Client()  # Creating an instance of MQTT client

client.connect(MQTT_Broker, MQTT_Port)  # Connecting the client to broker and port.

# This is an infinite loop that will detect motion and print either True Or False depend on if one has been detected
while True:

    motion_detected = random.choice([True, False])
    location_id = random.randint(0, 10)  # Selects a random number from the dictionary above

    location = location_map.get(location_id, "Unknown Location")  # This retrieves the location from the dictionary.
    # DEVICE CODE ENDS HERE
    day = date.today()  # date function call
    clock = datetime.now()  # time function calls
    time_time = datetime.time(clock)

    # convert to string to avoid type error when converting to json
    data_day = str(day)
    data_time = str(time_time)
    data = [location_id, location, motion_detected, data_day, data_time]
    """data = {
        "location_id": location_id,
        "location": location,
        "motion_detected": motion_detected,
        "Date": data_day,
        "Time": data_time
    }"""

    data_encoded = json.dumps(data)  # Coding data into json.

    current_time = datetime.now()   # The current date of how the data was sent.

    client.publish(MQTT_Topic, data_encoded)  # Publishing the data encoded to the mqtt topic.

    print(f"Just published: date-{current_time.date()} time-{current_time.time()}; data: {data_encoded} to topic: "
          f"'smarthouse/sensors/motion'")  # This will print the data and send it over to through the broker.

    time.sleep(random.randint(5, 10))  # This is a time sleep that will choose between 5,10 seconds when to send
    # This sends data between 5 and 10 seconds, and it will print either true or false.
