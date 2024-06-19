import subprocess
import webview # must be downloaded

pythontype = 'python'


# create subprocesses to run multiple files at once
file_1 = subprocess.Popen([pythontype, 'Publisher files/temp_sensors.py']) # subprocess for temp_sensors.py
file_2 = subprocess.Popen([pythontype, 'Database/main.py'])         # subprocess for main.py
file_3 = subprocess.Popen([pythontype, 'Database/database.py'])     # subprocess for database.py
file_4 = subprocess.Popen([pythontype, 'Website/Flask_code.py'])     # subprocess for login_page_flask.py
file_5 = subprocess.Popen([pythontype, 'Publisher files/camera.py'])     # subprocess for camera.py
file_6 = subprocess.Popen([pythontype, 'Publisher files/motionsensors.py'])     # subprocess for motionsensors.py
file_7 = subprocess.Popen([pythontype, 'Publisher files/bio_doorlock.py'])     # subprocess for bio_doorlock.py
file_8 = subprocess.Popen([pythontype, 'Publisher files/ChipMap.py'])     # subprocess for ChipMap.py
file_9 = subprocess.Popen([pythontype, 'Publisher files/SmartFridge.py'])     # subprocess for SmartFridge.py


# creates webview window at set size and opens index.html
window = webview.create_window("Inteligencia de Casa", 'http://localhost:4999/', width=400, height=800, resizable=False)

# Start the webview
webview.start()

# close all subprocesses on exit
file_1.wait()
file_2.wait()
file_3.wait()
file_4.wait()
file_5.wait()
file_6.wait()
file_7.wait()
file_8.wait()
file_9.wait()
