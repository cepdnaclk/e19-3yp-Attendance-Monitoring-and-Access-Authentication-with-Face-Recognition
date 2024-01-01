from gpiozero import MotionSensor
from attendance_recognition import capture_face,fingerprint_reader,pin_reader
from mqtt_communication import publish_msg
import os


pir = MotionSensor(4)
security_level = os.environ['SECURITY_LEVEL']


def motion_detector():
    while True:
        if pir.motion_detected:
            print("Motion Detected")

            if security_level == "easy":
                print("Easy Mode")

            elif security_level == "normal":
                print("Normal Mode")

                # find_f = 1
                find_f = fingerprint_reader.find_print()
                if find_f == -1:
                    print("No Fingerprint Detected")
                elif find_f == 1:
                    print("Fingerprint Detected")

            elif security_level == "hard":
                print("Hard Mode")
        else:
            print("No Motion")

