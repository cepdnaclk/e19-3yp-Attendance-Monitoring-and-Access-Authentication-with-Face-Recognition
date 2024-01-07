import os
from face_detection import capture_face
from control_logic import cmd_scripts
from mqtt_communication import publish_msg
from attendance_recognition import fingerprint_reader,pin_reader

#security_level = os.environ['SECURITY_LEVEL']
security_level = 'normal'
current_directory = os.path.dirname(os.path.realpath(__file__))
photo_storage_path = os.path.join(current_directory, '..', 'face_detection', 'captured')
photo_storage_path = os.path.abspath(photo_storage_path)  # Ensure the path is absolute


def easy_mode():
    print('----------------')
    print("Easy mode")
    print('----------------')

    try:
        capture_face.capture_face_detection(photo_storage_path)
        emp_id = cmd_scripts.recognize_faces()

        if emp_id is not None:
            msg = {
                "mode": "attendance",
                "id": emp_id,
                "sl": "easy",
                "cmd": "marked",
            }

            publish_msg.run(msg)
            return
    except Exception as e:
        print(e)


def normal_mode():
    print('----------------')
    print("Normal mode")
    print('----------------')

    try:
        capture_face.capture_face_detection(photo_storage_path)
        emp_id = cmd_scripts.recognize_faces()

        if emp_id is not None:
            msg = {
                "mode": "attendance",
                "id": emp_id,
                "sl": "normal",
                "cmd": "marked",
            }

            publish_msg.run(msg)

            status = fingerprint_reader.find_print()
            if status == 1:
                msg = {
                    "mode": "attendance",
                    "id": emp_id,
                    "sl": "normal",
                    "cmd": "fp_success",
                }

                publish_msg.run(msg)

    except Exception as e:
        print(e)


def hard_mode():
    print('----------------')
    print("Hard mode")
    print('----------------')

    try:
        capture_face.capture_face_detection(photo_storage_path)
        emp_id = cmd_scripts.recognize_faces()

        if emp_id is not None:
            msg = {
                "mode": "attendance",
                "id": emp_id,
                "sl": "normal",
                "cmd": "marked",
            }

            publish_msg.run(msg)

            status = fingerprint_reader.find_print()
            if status == 1:
                msg = {
                    "mode": "attendance",
                    "id": emp_id,
                    "sl": "normal",
                    "cmd": "fp_success",
                }

                publish_msg.run(msg)

                pin_code = pin_reader.get_pin()
                print("Pin code: {}".format(pin_code))

    except Exception as e:
        print(e)


def unlock_logic():
    if security_level == 'easy':
        easy_mode()
    elif security_level == 'normal':
        normal_mode()
    elif security_level == 'hard':
        hard_mode()