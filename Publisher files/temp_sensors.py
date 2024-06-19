import paho.mqtt.client as mqtt
import random
import time
from datetime import date, datetime
import json
import threading

# define heaters data and store in array
heater_1 = [1, "Bedroom 1", False]
heater_2 = [2, "Bedroom 2", False]
heater_3 = [3, "Bedroom 3", False]
heater_4 = [4, "Bedroom 4", False]
heater_5 = [5, "Upstairs corridor", False]
heater_6 = [6, "Kitchen", False]
heater_7 = [7, "Dining Room", False]
heater_8 = [8, "Living Room", False]
heater_9 = [9, "Study Room", False]
heater_10 = [10, "Entrance", False]

heaters = [heater_1, heater_2, heater_3, heater_4, heater_5, heater_6, heater_7, heater_8, heater_9, heater_10]

# define temperature sensor clients for each device and store in array
client = mqtt.Client("Temp_sensor_1")
client2 = mqtt.Client("Temp_sensor_2")
client3 = mqtt.Client("Temp_sensor_3")
client4 = mqtt.Client("Temp_sensor_4")
client5 = mqtt.Client("Temp_sensor_5")
client6 = mqtt.Client("Temp_sensor_6")
client7 = mqtt.Client("Temp_sensor_7")
client8 = mqtt.Client("Temp_sensor_8")
client9 = mqtt.Client("Temp_sensor_9")
client10 = mqtt.Client("Temp_sensor_10")

clients = [client, client2, client3, client4, client5, client6, client7, client8, client9, client10]

# declare temperature variables for sensors and store them in array
temp = 0
temp2 = 0
temp3 = 0
temp4 = 0
temp5 = 0
temp6 = 0
temp7 = 0
temp8 = 0
temp9 = 0
temp10 = 0

temps = [temp, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp9, temp10]


def main_1():
    # infinite loop to generate data from fake sensor devices
    while True:
        # DEVICE CODE STARTS HERE
        # 10 sensors
        global dev_numb
        dev_numb = random.randint(0, 9)  # gives random sensor number for ID and LOCATION from 10 different sensors
        # define client
        client = clients[dev_numb]
        client.connect("broker.hivemq.com", 1883) # connect to the broker on an appropriate port

        # initial variable declaration
        Id = 0
        location = ""

        # according to dev_numb declares Id number and location
        if dev_numb == 0:
            Id = 1
            location = "Bedroom 1"

        if dev_numb == 1:
            Id = 2
            location = "Bedroom 2"

        if dev_numb == 2:
            Id = 3
            location = "Bedroom 3"

        if dev_numb == 3:
            Id = 4
            location = "Bedroom 4"

        if dev_numb == 4:
            Id = 5
            location = "Upstairs corridor"

        if dev_numb == 5:
            Id = 6
            location = "Kitchen"

        if dev_numb == 6:
            Id = 7
            location = "Dining Room"

        if dev_numb == 7:
            Id = 8
            location = "Living Room"

        if dev_numb == 8:
            Id = 9
            location = "Study Room"

        if dev_numb == 9:
            Id = 10
            location = "Entrance"

        # TEMP CODE
        if temps[dev_numb] == 0:  # define initial temperature for sensor or if temp is 0
            init_temp = random.randint(10, 30)  # gives random number for temperature between 10 and 30 degrees
            temps[dev_numb] = init_temp

        # continues update of temp for previously published clients based on heater status
        if heaters[dev_numb][2] == True:
            temps[dev_numb] += 1
        if heaters[dev_numb][2] == False:
            temps[dev_numb] -= 1


        temp = temps[dev_numb]  # store sensor temp into variable to publish it

        # DEVICE CODE ENDS HERE
        day = date.today()  # date function call
        clock = datetime.now()  # time function calls
        time_time = datetime.time(clock)

        # convert to string to avoid type error when converting to json
        data_day = str(day)
        data_time = str(time_time)

        # store all data into array 'data'
        data = [Id, data_day, data_time, location, temp]
        # encode array 'data' into json data format to send it through topic
        data_encoded = json.dumps(data)

        # publish data to topics and print
        client.publish("smarthouse/temp/data", data_encoded)

        # print message with data, time and date to check if it is published
        print("Just published: date-" + str(day) + " time-" + str(time_time) + "; data: " + data_encoded +
              " to topic: 'smarthouse/temp/data'")

        # publish new entry between 3 and 10 seconds
        numb = random.randint(3, 10)
        time.sleep(numb)


def main_2():
    def on_connect(client, userdata, flags, rc):  # client method to connect

        if rc == 0:
            print("'Heaters' connected OK Returned code=", rc)  # let us know we connected to the broker
            # topic
            client.subscribe("smarthouse/heaters_db/status")
        else:
            print("Bad connection Returned code=", rc)  # if can't connect

    # function to receive messages
    def on_message(client, userdata, msg):  # client method to get messages from topic
        topic = msg.topic  # for use when we can't decode
        try:
            day = date.today()  # date function call
            clock = datetime.now()  # time function calls
            time_time = datetime.time(clock)

            # DECODING CODE GOES HERE FOR EACH SEPARATE TOPIC
            if topic == "smarthouse/heaters_db/status":  # decodes message from specific topic (sensors)
                data = json.loads(msg.payload.decode("utf-8"))  # decode message, turns it back into array 'data'

                # loop through all heaters and update all at once
                for i in range(len(heaters)):
                    if data[i][0] == 1:  # update heater on/off state according to received data
                        heaters[i][2] = True  # ( 1 = on/ True, 0 = off/ False)
                    else:
                        heaters[i][2] = False

            # print message with data, time and date to check if it is received and decoded
            print("Received message at 'Heaters': date-" + str(day) + " time-" + str(
                time_time) + " / data: topic: " + topic +
                  ";  value: " + str(data))

        except:
            print(
                "Cannot decode data on topic:" + topic)  # cannot decode; print the topic for the non-decodable message

    # define client
    client = mqtt.Client()
    # callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("broker.hivemq.com", 1883) # connect to the broker on an appropriate port

    client.loop_forever() # keep looping forever (allows realtime subscription)


send_generated = threading.Thread(target=main_1)
receive_heaters_data = threading.Thread(target=main_2)

send_generated.start()
receive_heaters_data.start()

send_generated.join()
receive_heaters_data.join()
