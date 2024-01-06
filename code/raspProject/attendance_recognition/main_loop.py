from gpiozero import MotionSensor
from attendance_recognition import capture_face, fingerprint_reader, pin_reader
from mqtt_communication import publish_msg
import os

pir = MotionSensor(4)
security_level = os.environ['SECURITY_LEVEL']


def motion_detector():
    while True:
        if pir.motion_detected:
            print("Motion Detected")
        else:
            print("No Motion")
