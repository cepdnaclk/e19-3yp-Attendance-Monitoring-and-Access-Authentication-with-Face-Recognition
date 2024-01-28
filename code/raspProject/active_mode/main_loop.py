from gpiozero import MotionSensor
from active_mode import active_handler
import time

pir = MotionSensor(4)


def motion_detector(queue):
    if pir.motion_detected:
        print("Motion Detected")
        queue.put('Motion Detected')
        active_handler.attendance_handler(queue)
        time.sleep(10)

    else:
        print("No Motion")
        queue.put('No Motion')
        time.sleep(5)
