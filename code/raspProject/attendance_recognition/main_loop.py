from gpiozero import MotionSensor
from attendance_recognition import capture_face, fingerprint_reader, pin_reader
from mqtt_communication import publish_msg
import os
import time

pir = MotionSensor(4)
#security_level = os.environ['SECURITY_LEVEL']


def motion_detector():
    if pir.motion_detected:
        print("Motion Detected")
        time.sleep(1)

    else:
        print("No Motion")
        time.sleep(1)
