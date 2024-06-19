import paho.mqtt.client as mqtt
import sqlite3 # import sqlite
from datetime import date, datetime
import json

# function to connect with topic
def on_connect(client, userdata, flags, rc):  # client method to connect

    if rc == 0:
        print("connected OK Returned code=", rc)  # let us know we connected to the broker

        # TOPICS MUST BE ADDED HERE
        client.subscribe("smarthouse/temp/data")
        client.subscribe("smarthouse/sensors/motion")
        client.subscribe("smarthouse/cameras/data")
        client.subscribe("smarthouse/doorlock/data")
        client.subscribe("smarthouse/chip/data")
        client.subscribe("smarthouse/fridge/data")

    else:
        print("Bad connection Returned code=", rc)  # if we can't connect


# function to receive messages
def on_message(client, userdata, msg,):  # client method to get messages from topic
    topic = msg.topic  # for use when we can't decode

    try:
        day = date.today()  # date function call
        clock = datetime.now()  # time function calls
        time_time = clock.strftime("%H:%M:%S") # Just in H-M-S format

        # DECODING CODE GOES HERE FOR EACH SEPARATE TOPIC
        if topic == "smarthouse/temp/data":                   # decodes message from specific topic (sensors)
            data = json.loads(msg.payload.decode("utf-8"))       # decode message, turns it back into array 'data'

            # insert data into database
            connect_db = sqlite3.connect('Database/database.db') # connect to database
            cursor = connect_db.cursor()                         # define cursor
            # transfer data from array to new row in the temperature_sensors table
            cursor.execute("""UPDATE temperature_sensors
                                SET DATE = ?, TIME = ?, TEMPERATURE = ?
                                WHERE ID = ?;""", (data[1], data[2], data[4], data[0]))

            connect_db.commit() # commit changes to database
            connect_db.close()  # close database
       # Zeyd's
        if topic == "smarthouse/cameras/data":                   # decodes message from specific topic (sensors)
            data = json.loads(msg.payload.decode("utf-8"))       # decode message, turns it back into array 'data'

            # stores data from arrays to variables
            Id = data[0]
            status = data[1]
            location = data[2]
            day = data[3]
            time_time = data[4]
            #video_data = bytearray(data[5])

            try:
                # Connecting to the database
                conn = sqlite3.connect('Database/database.db')
                cursor = conn.cursor()

                cursor.execute('''CREATE TABLE IF NOT EXISTS Camera(
                id INTEGER,
                Cam_Status VARCHAR(5),
                Cam_Location VARCHAR(20),
                Clip_Date DATE,
                Clip_Time TIME,
                Clip BLOB
                );'''
                )

                cursor.execute('''INSERT INTO Camera VALUES (
                               :id, 
                               :Cam_Status, 
                               :Cam_location, 
                               :Clip_Date, 
                               :Clip_Time, 
                               NULL)''', {
                    "id": Id,
                    "Cam_Status": status,
                    "Cam_location": location,
                    "Clip_Date": day,
                    "Clip_Time": time_time
                    #"Clip": str(video_data)
                })
                conn.commit()
                conn.close()
                print("Succesfully inserted in database. \n")
                
            except Exception as e:
                print(f"Failed to insert in database. Error: {str(e)}\n")
            
            '''try:
                # Decoding the video file
                output_path = '/Users/zeydajraou/Documents/IDC/Decoded/output_photo.jpeg'

                with open(output_path, 'wb') as video_file:
                    video_file.write(video_data)
                print(f"Video Successfully decoded in folder {output_path}\n")

            except Exception as e:
                print(f"Failed to decode the video. Error: {str(e)}\n")'''


            # Stefan's
        if topic == "smarthouse/sensors/motion":
            data = json.loads(msg.payload.decode("utf-8"))
            connect_db = sqlite3.connect('Database/database.db')
            cursor = connect_db.cursor()
            try:
                cursor.execute("""CREATE TABLE IF NOT EXISTS motion_sensors( 
                    LocationID INTEGER, 
                    Location VARCHAR(255), 
                    STATUS BIT,
                    Date DATE,
                    Time TIME
                );""")
            except sqlite3.Error as e:
                print("Error creating table:", e)

            cursor.execute("INSERT INTO motion_sensors VALUES (:LocationID, :Location, :Status, :Date, :Time)", {
                "LocationID": data[0],
                "Location": data[1],
                "Status": data[2],
                "Date": data[3],
                "Time": data[4]
            })
            connect_db.commit()
            connect_db.close()
            
           #Milo
        if topic == "smarthouse/doorlock/data":                   # decodes message from specific topic (sensors)
            data = json.loads(msg.payload.decode("utf-8"))      # decode message, turns it back into array 'data'

            connection = sqlite3.connect('Database/database.db')
            cursor = connection.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS fingerprints(
            uniqueid INTEGER PRIMARY KEY AUTOINCREMENT,
            fingers TEXT,
            opendate DATE NOT NULL,
            opentime DATETIME NOT NULL,
            success_or_fail BOOLEAN NOT NULL
            );'''
            )
            # stores data from arrays to variables
            fingerprint = data[0]                                         # example: database.Id = data[0]
            lock_action = data[1]
            #timestamp = data[2]                                  # redundant will grab current date and time from current file

            sql_fingerprint_insertion = """INSERT INTO fingerprints (fingers, opendate, opentime, success_or_fail) 
                                                       VALUES (?, ?, ?, ?)"""

            fingerprintvalues = (fingerprint, day, str(time_time), lock_action)

            cursor.execute(sql_fingerprint_insertion, fingerprintvalues)
            connection.commit()

            print("Data submitted to database")

            cursor.close()
            connection.close()

           # Aymen
        if topic == "smarthouse/chip/data":
            data = json.loads(msg.payload.decode("utf-8"))
        
         # Troy 
          

        if topic == "smarthouse/fridge/data":
            conn = sqlite3.connect('Database/database.db')
            c = conn.cursor()

            c.execute('''CREATE TABLE IF NOT EXISTS fridge_data
               (humidity REAL, doorstatus TEXT, temperature REAL, fridgeid TEXT)''') 

            data = json.loads(msg.payload.decode("utf-8"))
            humidity = data[0]
            doorstatus = data[1]
            temperature = data[2]
            fridgeid = data[3]

            c.execute("INSERT INTO fridge_data (humidity, doorstatus, temperature, fridgeid) VALUES (?, ?, ? ,?)",
              (humidity, doorstatus, temperature,fridgeid))

            conn.commit()
            print("Data added to the database successfully.")
            conn.close()



        # print message with data, time and date to check if it is received and decoded
        print("Received message at : date-" + str(day) + " time-" + str(time_time) + " / data: topic: " + topic + ";  value: \n"
              '''+ str(data)''')
        


             



    except:
        print("Cannot decode data on topic:" + topic)  # cannot decode; print the topic for the non-decodable message

#define client
client = mqtt.Client()

#callback functions
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883)  # connect to the broker on an appropriate port

client.loop_forever()  # keep looping forever (allows realtime subscription)
