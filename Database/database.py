import paho.mqtt.client as mqtt
import sqlite3
import time
import json
from datetime import date, datetime
import sys
sys.path.append('../Website')
from Website.variables_module import max_temperature, min_temperature

#define client
client = mqtt.Client("Heating_database")
client.connect("broker.hivemq.com", 1883) # connect to the broker on an appropriate port

connect_db = sqlite3.connect('Database/database.db')  # connect to database
cursor = connect_db.cursor()                 # define cursor

# create temperature_sensors table and heating_central tables
cursor.execute("""CREATE TABLE IF NOT EXISTS temperature_sensors(
ID INTEGER,
DATE DATE,
TIME TIME,
LOCATION Text,
TEMPERATURE INTEGER
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS heating_central(
ID INTEGER,
LOCATION text,
STATUS BIT 
);""")

# select full count of all rows in heating_central
cursor.execute("""SELECT COUNT(*) FROM heating_central""")
entries = cursor.fetchone()[0]

if entries == 0:             # run this code if there is 0 rows in heating_central

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

    for i in range(len(heaters)): # add rows in heating_central, one for each heater
        cursor.execute("INSERT INTO heating_central VALUES (:ID, :LOCATION, :STATUS)", {
            "ID": heaters[i][0],
            "LOCATION": heaters[i][1],
            "STATUS": heaters[i][2]
        })

# select full count of all rows in temperature_sensors
cursor.execute("""SELECT COUNT(*) FROM temperature_sensors""")
entries = cursor.fetchone()[0]

if entries == 0:             # run this code if there is 0 rows in temperature_sensors
    # define heaters data and store in array
    temp_sensor_1 = [1, "2024-03-22", "00:00:00.000000", "Bedroom 1", 17]
    temp_sensor_2 = [2, "2024-03-22", "00:00:00.000000", "Bedroom 2", 17]
    temp_sensor_3 = [3, "2024-03-22", "00:00:00.000000", "Bedroom 3", 17]
    temp_sensor_4 = [4, "2024-03-22", "00:00:00.000000", "Bedroom 4", 17]
    temp_sensor_5 = [5, "2024-03-22", "00:00:00.000000", "Upstairs corridor", 17]
    temp_sensor_6 = [6, "2024-03-22", "00:00:00.000000", "Kitchen", 17]
    temp_sensor_7 = [7, "2024-03-22", "00:00:00.000000", "Dining Room", 17]
    temp_sensor_8 = [8, "2024-03-22", "00:00:00.000000", "Living Room", 17]
    temp_sensor_9 = [9, "2024-03-22", "00:00:00.000000", "Study Room", 17]
    temp_sensor_10 = [10, "2024-03-22", "00:00:00.000000", "Entrance", 17]

    temp_sensors = [temp_sensor_1, temp_sensor_2, temp_sensor_3, temp_sensor_4, temp_sensor_5, temp_sensor_6,
                    temp_sensor_7, temp_sensor_8, temp_sensor_9, temp_sensor_10]

    for i in range(len(temp_sensors)): # add rows in heating_central, one for each heater
        cursor.execute("INSERT INTO temperature_sensors VALUES (:ID, :DATE, :TIME, :LOCATION, :TEMPERATURE)", {
            "ID": temp_sensors[i][0],
            "DATE": temp_sensors[i][1],
            "TIME": temp_sensors[i][2],
            "LOCATION": temp_sensors[i][3],
            "TEMPERATURE": temp_sensors[i][4]
        })

connect_db.commit()  # commit changes to database
connect_db.close()  # close database

def update_heaters_on(cursor):   # join query to update heater status to 1 (True) if temperature drops below 15 degrees
    cursor.execute("""  UPDATE heating_central AS h1
                        SET STATUS = 1
                        WHERE h1.ID IN (
                            SELECT ts.ID
                            FROM temperature_sensors AS ts
                            WHERE ts.TEMPERATURE < ?);""", (min_temperature,))

def update_heaters_off(cursor):  # join query to update heater status to 0 (False) if temperature climbs above 25 degrees
    cursor.execute("""  UPDATE heating_central AS h1
                            SET STATUS = 0
                            WHERE h1.ID IN (
                                SELECT ts.ID
                                FROM temperature_sensors AS ts
                                WHERE ts.TEMPERATURE > ?);""", (max_temperature,))

def send_back(cursor):  # query to collect heater data and send it device to update "physical" device
    cursor.execute(""" SELECT STATUS FROM heating_central """)
    data = cursor.fetchall()       # fetch all data from query

    # encode array 'data' into json data format to send it through topic
    data_encoded = json.dumps(data)

    day = date.today()  # date function call
    clock = datetime.now()  # time function calls
    time_time = datetime.time(clock)

    # publish data to topics and print
    client.publish("smarthouse/heaters_db/status", data_encoded)

    # print message with data, time and date to check if it is published
    print("Just published: date-" + str(day) + " time-" + str(time_time) + "; data: " + data_encoded +
          " to topic: 'smarthouse/heaters_db/status'")


# main loop
def main():
    while True:
        connect_db = sqlite3.connect('Database/database.db')  # connect to database
        cursor = connect_db.cursor()  # define cursor

        # run all functions
        update_heaters_on(cursor)
        update_heaters_off(cursor)
        send_back(cursor)

        connect_db.commit()  # commit changes to database
        connect_db.close()  # close database

        time.sleep(20)  # run loop every 10 second

main()




