#Import all neccessary features to code.
import RPi.GPIO as GPIO
from time import sleep

#If code is stopped while the solenoid is active it stays active
#This may produce a warning if the code is restarted and it finds the GPIO Pin, which it defines as non-active in next line, is still active
#from previous time the code was run. This line prevents that warning syntax popping up which if it did would stop the code running.
GPIO.setwarnings(False)
#This means we will refer to the GPIO pins
#by the number directly after the word GPIO. A good Pin Out Resource can be found here https://pinout.xyz/
GPIO.setmode(GPIO.BCM)       
#This sets up the GPIO 25 pin as an output pin
GPIO.setup(19,GPIO.OUT)


def open_lock(queue):
    print('Door Unlocked!')
    queue.put('Door Unlocked!')
    GPIO.output(19,0)
    
    payload = {
        'device_id': 1,
        'lock_state': True
    }
    
    #backend_url = 'https://facesecure.azurewebsites.net/attendanceManagement/save-device-lock/'
    #response = requests.post(backend_url, json=payload)
    #response = requests.post(backend_url, json=payload)
    sleep(5)
    queue.put('Welcome')
    GPIO.output(19,1)
