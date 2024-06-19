###  CODE SET UP TO BE RUN FROM EXEC_ALL.PY

from flask import Flask, send_from_directory, render_template, request, redirect, url_for
import sqlite3
import variables_module
import folium 

# declare Flask with custom folder directories
app = Flask(__name__, template_folder='../Website', static_folder='../Website')


# LOGIN PAGE CODE

# render login page
@app.route('/')
def update_index_page():
        return render_template('index.html')


# fetch login page from directory
@app.route('/login.html')
def serve_html_index():
    return send_from_directory(app.template_folder, 'index.html')


# fetch login page css to render it with the page
@app.route('/style.css')
def serve_css_style():
    return send_from_directory(app.static_folder, 'style.css')


# user login and password details
credentials = {
    "admin": "qwerty",
    "test": "password"
}


# converted Javascript code to Python Flask to verify user details and switch to different page
@app.route('/login', methods=['POST'])
def login():
    # fetch details from html form
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username exists in the credentials dictionary
    if username in credentials and credentials[username] == password:
        # Redirect to the device page upon successful login
        return redirect(url_for('update_page'))
    else:
        # Render the login page with an error message
        return render_template('index.html', error="Invalid username or password")
    
# Fridge.html /Troy 

@app.route('/Fridge.html')
def update_fridge_page():
    connect_db = sqlite3.connect('Database/database.db')
    cursor = connect_db.cursor()
    data = fetch_fridge_data(cursor)
    connect_db.close()
    
    # Extracting individual data components
    humidity = data[0][0]
    status = data[0][1]
    temperature = data[0][2]
    fridgeid = data[0][3]  
    return render_template('Fridge.html',
                           humidity=humidity,
                           status=status,
                           temperature=temperature,
                           fridgeid = fridgeid) 

def fetch_fridge_data(cursor):
    cursor.execute("""SELECT humidity, Doorstatus, Temperature, fridgeid 
                   FROM fridge_data 
                   ORDER BY fridgeid DESC
                   LIMIT 1 ;""")
    return cursor.fetchall()

@app.route('/troyreload')
def troyreload():
    return redirect(url_for('update_fridge_page')) 
@app.route('/Fridge.css')
def Tserve_css_temp():
    return send_from_directory(app.static_folder,'Fridge.css')





# MOTION SENSORS PAGE / Stefan
def fetch_web_mdata(cursor):
    cursor.execute("""SELECT ms.Location, 
                            ms.Status,
                            CASE
                                WHEN Status = 1 THEN 'ON'
                                ELSE 'OFF'
                            END
                            FROM motion_sensors ms
                            ORDER BY ms.Date DESC, ms.Time DESC
                            LIMIT 5;""")
    return cursor.fetchall()



# function which renders a temp_sensors page and fetch SQL query data and places data on page based on keys
@app.route('/motionsensors.html')
def update_mpage():
    connect_db = sqlite3.connect('Database/database.db')
    cursor = connect_db.cursor()
    data = fetch_web_mdata(cursor)
    print(data)
    connect_db.commit()  # commit changes to database
    connect_db.close()  # close database
    return render_template(
    'motionsensors.html',
                      mlocation_1=data[0][0],
                      status_1=data[0][1],
                      mlocation_2=data[1][0],
                      status_2=data[1][1],
                      mlocation_3=data[2][0],
                      status_3=data[2][1],
                      mlocation_4=data[3][0],
                      status_4=data[3][1],
                      mlocation_5=data[4][0],
                      status_5=data[4][1])
@app.route('/mreload')
def mreload():
    return redirect(url_for('update_mpage'))

@app.route('/motionsensors.css')
def mserve_css_temp():
    return send_from_directory(app.static_folder, 'motionsensors.css')

# TEMP_SENSORS PAGE

# SQL query to fetch required data for temp_sensors page
def fetch_web_data(cursor):
    cursor.execute("""SELECT ts.LOCATION,
                          ts.DATE,
                          strftime('%H:%M:%S', ts.TIME),
                          ts.TEMPERATURE,
                          CASE
                                WHEN h.STATUS = 1 THEN 'ON'
                                ELSE 'OFF'
                          END
                          FROM temperature_sensors ts
                          JOIN heating_central h ON ts.ID = h.ID
                          ORDER BY ts.DATE DESC,ts.TIME DESC
                          LIMIT 7;""")
    return cursor.fetchall()

# function which renders a temp_sensors page and fetch SQL query data and places data on page based on keys


# function which renders a temp_sensors page and fetch SQL query data and places data on page based on keys
@app.route('/temp_sensors.html')
def update_page():
        connect_db = sqlite3.connect('Database/database.db')
        cursor = connect_db.cursor()
        data = fetch_web_data(cursor)
        connect_db.commit()  # commit changes to database
        connect_db.close()  # close database
        return render_template(
                                'temp_sensors.html',
                                location_1=data[0][0],
                                time_1=data[0][2],
                                temperature_1=data[0][3],
                                heater_1=data[0][4],
                                location_2=data[1][0],
                                time_2=data[1][2],
                                temperature_2=data[1][3],
                                heater_2=data[1][4],
                                location_3=data[2][0],
                                time_3=data[2][2],
                                temperature_3=data[2][3],
                                heater_3=data[2][4],
                                location_4=data[3][0],
                                time_4=data[3][2],
                                temperature_4=data[3][3],
                                heater_4=data[3][4],
                                location_5=data[4][0],
                                time_5=data[4][2],
                                temperature_5=data[4][3],
                                heater_5=data[4][4],
                                location_6=data[5][0],
                                time_6=data[5][2],
                                temperature_6=data[5][3],
                                heater_6=data[5][4],
                                location_7=data[6][0],
                                time_7=data[6][2],
                                temperature_7=data[6][3],
                                heater_7=data[6][4]
                                   )

# fetch temp_sensors css to render it with the page
@app.route('/temp_sensors.css')
def serve_css_temp():
    return send_from_directory(app.static_folder, 'temp_sensors.css')

@app.route('/reload')
def reload():
    return redirect(url_for('update_page'))

@app.route('/digital.ttf')
def serve_font_meter():
    return send_from_directory(app.static_folder, 'digital.ttf')

@app.route('/Heat.ttf')
def serve_font_temp_title():
    return send_from_directory(app.static_folder, 'Heat.ttf')

from variables_module import max_temperature, min_temperature
@app.route('/change_temp', methods=['POST'])
def change_temp():
    # fetch details from html form
    max_temp = request.form.get('max_temp')
    min_temp = request.form.get('min_temp')

    #
    if max_temp.isdigit() and min_temp.isdigit():
        variables_module.max_temperature = max_temp
        variables_module.min_temperature = min_temp
        return redirect(url_for('update_page'))

    else:
        # Render the login page with an error message
        return render_template('temp_sensors.html', error="Invalid input type")


# Cameras / Zeyd

@app.route('/creload')
def creload():
    return redirect(url_for('update_cpage'))

@app.route('/cameras.css')
def cserve_css_temp():
    return send_from_directory(app.static_folder, 'cameras.css')

def fetch_web_cdata(cursor):
    cursor.execute("""SELECT subquery.id, subquery.Cam_location, subquery.Clip_Date, subquery.Clip_Time
                            FROM (
                                SELECT c.id, c.Cam_Location, c.Clip_Date, c.Clip_Time,
                                    ROW_NUMBER() OVER (PARTITION BY c.id ORDER BY c.Clip_Date DESC, c.Clip_Time DESC) AS row_num
                                FROM camera c
                            ) AS subquery
                            WHERE subquery.row_num = 1
                            ORDER BY subquery.id;""")
    return cursor.fetchall()

@app.route('/cameras.html')
def update_cpage():
    connect_db = sqlite3.connect('Database/database.db')
    cursor = connect_db.cursor()
    data = fetch_web_cdata(cursor)
    print(data)
    connect_db.commit()  # commit changes to database
    connect_db.close()  # close database
    return render_template(
    'cameras.html',
                    clocation_1=data[0][1],
                    cdate_1=data[0][2],
                    ctime_1=data[0][3],
                    clocation_2=data[1][1],
                    cdate_2=data[1][2],
                    ctime_2=data[1][3],
                    clocation_3=data[2][1],
                    cdate_3=data[2][2],
                    ctime_3=data[2][3],
                    clocation_4=data[3][1],
                    cdate_4=data[3][2],
                    ctime_4=data[3][3],
                    clocation_5=data[4][1],
                    cdate_5=data[4][2],
                    ctime_5=data[4][3])

@app.route('/Camera_Image1.html')
def open_img1():
    return render_template('Camera_Image1.html')

@app.route('/Camera_Image2.html')
def open_img2():
    return render_template('Camera_Image2.html')

@app.route('/Camera_Image3.html')
def open_img3():
    return render_template('Camera_Image3.html')

@app.route('/Camera_Image4.html')
def open_img4():
    return render_template('Camera_Image4.html')

@app.route('/Camera_Image5.html')
def open_img5():
    return render_template('Camera_Image5.html')

# Door Lock / Milo
@app.route('/door_lock.css')
def lockserve_css_temp():
    return send_from_directory(app.static_folder, 'door_lock.css')

@app.route('/lockreload')
def lockreload():
    return redirect(url_for('update_door_lock_page'))

def fetch_web_ldata(cursor):
    cursor.execute("""SELECT *,
                      CASE
                      WHEN success_or_fail = 1 THEN 'Unlocked'
                      WHEN success_or_fail = 0 THEN 'Locked'
                      ELSE 'Unknown'
                      END AS status
                      FROM fingerprints
                      ORDER BY uniqueid DESC
                      LIMIT 5;
                      """)
    return cursor.fetchall()

@app.route('/door_lock.html')
def update_door_lock_page():
    connect_db = sqlite3.connect('Database/database.db')
    cursor = connect_db.cursor()
    data = fetch_web_ldata(cursor)
    connect_db.close()
    return render_template('door_lock.html',
                           uniqueid1= data[0][0],
                           fingers1= data[0][1],
                           opendate1= data[0][2],
                           opentime1= data[0][3],
                           success_or_fail1= data[0][4],

                           uniqueid2=data[1][0],
                           fingers2=data[1][1],
                           opendate2=data[1][2],
                           opentime2=data[1][3],
                           success_or_fail2=data[1][4],

                           uniqueid3 = data[2][0],
                           fingers3 = data[2][1],
                           opendate3 = data[2][2],
                           opentime3 = data[2][3],
                           success_or_fail3 = data[2][4])


#CHIP / Aymen
# Function to fetch coordinates from the database
def fetch_coordinates_from_db():
    conn = sqlite3.connect("Database/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Latitude, Longitude FROM Chip")
    coordinates = cursor.fetchall()
    conn.close()
    return coordinates

# Function to visualize coordinates on the map
def visualize_coordinates_on_map(coordinates):
    map = folium.Map(location=[52.178219, -1.667904], zoom_start=15)

    # Add markers for each coordinate on map
    for coord in coordinates:
        folium.Marker([coord[0], coord[1]]).add_to(map)

    # Save the map to an HTML file
    map_filename = 'Website/map.html'
    map.save(map_filename)
    print("Map updated and saved to:", map_filename)

# Route to update the map with new coordinates
@app.route('/chip.html')
def load_map():
    return render_template('chip.html')

@app.route('/update_map')
def update_map():
    # Fetch coordinates from the database
    coordinates = fetch_coordinates_from_db()
    # Visualize coordinates on the map
    visualize_coordinates_on_map(coordinates)
    return load_map()


# HEADER AND FOOTER
# fetch header and footer css to render it with the page
@app.route('/frame.css')
def serve_css_frame():
    return send_from_directory(app.static_folder, 'frame.css')

# fetch logo to render it with the page
@app.route('/logo.png')
def serve_logo():
    return send_from_directory(app.static_folder, 'logo.png')

# fetches fonts to render them with the page
@app.route('/OTF.otf')
def serve_font_title():
    return send_from_directory(app.static_folder, 'OTF.otf')

@app.route('/drop_font.otf')
def serve_font_drop():
    return send_from_directory(app.static_folder, 'drop_font.otf')

# main loop
def main():

    app.run(host='localhost', port=4999)     # run Flask with host = 'localhost', port = 5000 to match webview window

main()