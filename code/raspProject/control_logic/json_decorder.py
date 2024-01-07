import json
from control_logic import cmd_scripts
import os
from config_logic import make_folder
from face_detection import capture_face
from attendance_recognition import fingerprint_reader,pin_reader
from mqtt_communication import publish_msg
from cryptography.fernet import Fernet

key = Fernet.generate_key()
key_str = key.decode('utf-8')
os.environ["KEY"] = key_str
cipher_suite = Fernet(key)


def encrypt_pin(pin_code):
    # Encrypt the PIN code
    encrypted_pin = cipher_suite.encrypt(pin_code.encode())
    return encrypted_pin


def json_decorator(msg):
    payload = msg.payload.decode()
    try:
        json_payload = json.loads(payload)
        # Now `json_payload` is a Python dictionary containing the parsed JSON data
        # You can access values using keys, e.g., json_payload["key"]

        if json_payload.get("mode", "").lower() == "configure":
            print("Configuration Mode Activated")

            if json_payload.get("cmd", "").lower() == "change_level":
                print("Changing Security Level to", json_payload.get("sl", "").lower())
                os.environ["SECURITY_LEVEL"] = json_payload.get("sl", "").lower()
                print("Security Level (changed):", os.environ["SECURITY_LEVEL"])

            if json_payload.get("cmd", "").lower() == "update_device":
                print("Running Device Database Update...")
                cmd_scripts.encode_faces()

            if json_payload.get("cmd", "").lower() == "capture_image":
                print("Getting Ready for capturing images...")
                folder_name = json_payload.get("name", "").lower()
                emp_id = json_payload.get("id", "")
                print("Making folder...", folder_name)
                folder_path = make_folder.create_folder(folder_name)
                try:
                    status = capture_face.capture_face_storing(folder_name, folder_path)

                    if status:
                        msg = {
                            "mode": "configure",
                            "id": emp_id,
                            "name": json_payload.get("name", ""),
                            "cmd": "face_successful",
                        }
                    else:
                        msg = {
                            "mode": "configure",
                            "id": emp_id,
                            "name": json_payload.get("name", ""),
                            "cmd": "face_unsuccessful",
                        }
                    publish_msg.run(msg)

                except Exception as e:
                    print(e)

            if json_payload.get("cmd", "").lower() == "capture_fp":
                print("Getting Ready for capturing finger print...")
                emp_id = json_payload.get("id", "")
                try:
                    status = fingerprint_reader.enroll_finger(emp_id)

                    if status:
                        msg = {
                            "mode": "configure",
                            "id": emp_id,
                            "name": json_payload.get("name", ""),
                            "cmd": "fp_successful",
                        }
                    else:
                        msg = {
                            "mode": "configure",
                            "id": emp_id,
                            "name": json_payload.get("name", ""),
                            "cmd": "fp_unsuccessful",
                        }
                    publish_msg.run(msg)

                except Exception as e:
                    print(e)

            if json_payload.get("cmd", "").lower() == "capture_pin":
                print("Getting Ready for capturing PIN...")
                emp_id = json_payload.get("id", "")
                try:
                    pin_code = pin_reader.get_pin()
                    en_pin = encrypt_pin(pin_code)
                    print(en_pin)

                    msg = {
                        "mode": "configure",
                        "id": emp_id,
                        "name": json_payload.get("name", ""),
                        "cmd": "pin_successful",
                        "pin": en_pin
                    }
                    publish_msg.run(msg)

                except Exception as e:
                    print(e)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")