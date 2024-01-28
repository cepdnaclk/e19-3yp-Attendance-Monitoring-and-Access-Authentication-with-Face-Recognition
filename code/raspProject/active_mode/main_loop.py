from gpiozero import MotionSensor
from active_mode import active_handler
import time

pir = MotionSensor(4)


def motion_detector():
    if pir.motion_detected:
        print("Motion Detected")
        active_handler.attendance_handler()
        time.sleep(1)

    else:
        print("No Motion")
        time.sleep(1)
