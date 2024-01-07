from gpiozero import MotionSensor
from attendance_recognition import unlock_logic
import time

pir = MotionSensor(4)


def motion_detector():
    if pir.motion_detected:
        print("Motion Detected")
        unlock_logic.unlock_logic()
        time.sleep(1)

    else:
        print("No Motion")
        time.sleep(1)
