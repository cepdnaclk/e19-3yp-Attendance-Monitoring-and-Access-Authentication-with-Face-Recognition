import os
from attendance_recognition import capture_face, fingerprint_reader, pin_reader
from mqtt_communication import publish_msg
from face_detection import capture_face
from control_logic import cmd_scripts

#security_level = os.environ['SECURITY_LEVEL']
security_level = 'easy'


def easy_mode():
    print('----------------')
    print("Easy mode")
    print('----------------')

    capture_face.capture_face_detection()
    name = cmd_scripts.recognize_faces()

    if name is not None:
        return 1
    else:
        return 0


def normal_mode():
    print("Normal mode")


def hard_mode():
    print("Hard mode")


def unlock_logic():
    if security_level == 'easy':
        easy_mode()

'''
def unlock_logic():
    if security_level == "easy":
        print("Easy Mode")

        msg = {
            "mode": "att_marking",
            "sl": "easy",
            "id": "001",
            "name": "asela_hemantha",
            "cmd": "marked",
        }

        publish_msg.run(msg)

        # face capture

    elif security_level == "normal":
        print("Normal Mode")

        # face capture

        msg = {
            "mode": "att_marking",
            "sl": security_level,
            "id": "001",
            "name": "asela_hemantha",
            "cmd": "marked",
        }

        publish_msg.run(msg)

        find_f = fingerprint_reader.find_print()
        if find_f == 0:
            print("No Fingerprint Detected")

            msg = {
                "mode": "att_marking",
                "sl": security_level,
                "id": "001",
                "name": "asela_hemantha",
                "cmd": "fp_failed",
            }

            publish_msg.run(msg)

        elif find_f == 1:
            print("Fingerprint Detected")

            msg = {
                "mode": "att_marking",
                "sl": security_level,
                "id": "001",
                "name": "asela_hemantha",
                "cmd": "fp_success",
            }

            publish_msg.run(msg)

    elif security_level == "hard":
        print("Hard Mode")

        # face capture
        msg = {
            "mode": "att_marking",
            "sl": security_level,
            "id": "001",
            "name": "asela_hemantha",
            "cmd": "marked",
        }

        publish_msg.run(msg)

        find_f = fingerprint_reader.find_print()
        if find_f == -1:
            print("No Fingerprint Detected")

            msg = {
                "mode": "att_marking",
                "sl": security_level,
                "id": "001",
                "name": "asela_hemantha",
                "cmd": "fp_failed",
            }

            publish_msg.run(msg)

        elif find_f == 1:
            print("Fingerprint Detected")

            msg = {
                "mode": "att_marking",
                "sl": security_level,
                "id": "001",
                "name": "asela_hemantha",
                "cmd": "fp_success",
            }

            publish_msg.run(msg)

        pincode = pin_reader.get_pin_from_keypad()
        print("Entered PIN code:", pincode)
'''
