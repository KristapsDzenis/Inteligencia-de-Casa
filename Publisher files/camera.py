import paho.mqtt.client as mqtt
import random
import time
from datetime import date, datetime
import json

# define client
client = mqtt.Client("cameras")

# connect to the broker on an appropriate port
client.connect("broker.hivemq.com", 1883)

# infinite loop to generate data from fake sensor devices
while True:
    # DEVICE CODE STARTS HERE
    # 5 cameras
    Id_numb = random.randint(1, 5) # gives random sensor number for ID and LOCATION from 5 different cameras

    Id = 1
    location = ""  # This will tell us where the camera is placed in the house
    status = "ON"  # This will tell us if the camera is On or Off

    #with open('../IDC/IDC_Test_Photo.jpeg', 'rb') as video_file:
        #video_content = video_file.read()


    # according to Id_numb declares which camera publish data
    if Id_numb == 1:
        Id = 1
        location = "Home_Front"

    if Id_numb == 2:
        Id = 2
        location = "Home_Back"

    if Id_numb == 3:
        Id = 3
        location = "Driveway"

    if Id_numb == 4:
        Id = 4
        location = "Entrance"

    if Id_numb == 5:
        Id = 5
        location = "Upstairs"


    # DEVICE CODE ENDS HERE
        
    day = date.today()  # date function call
    clock = datetime.now()  # time function calls
    time_time = clock.strftime("%H:%M:%S") # Just in H-M-S format

    # store all data into array 'data'
    data = [Id, status, location, str(day), str(time_time)]#, list(video_content)]

    # encode array 'data' into json data format to send it through topic
    data_encoded = json.dumps(data)

    # publish data to topics and print
    client.publish("smarthouse/cameras/data", data_encoded)

    # print message with data, time and date to check if it is published
    print("Just published: id- " + str(Id) + "; status- " + str(status) + "; day- " + str(day) + "; time- " + str(time_time) +
          " to topic: 'smarthouse/cameras/data'\n")

    # waits 10 seconds before publishing again
    time.sleep(10)

