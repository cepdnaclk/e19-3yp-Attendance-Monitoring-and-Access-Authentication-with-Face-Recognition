import json
import os
from mqtt_communication import publish_msg
from components import fingerprint, camera, keypad
from configuration_mode import send_request

security_level = os.getenv('SECURITY_LEVEL')


def json_handler(json_payload):
    # `json_payload` is a Python dictionary containing the parsed JSON data
    # You can access values using keys, e.g., json_payload["key"]

    if json_payload.get("mode", "").lower() == "configure":

        # Change the security level
        if json_payload.get("cmd", "").lower() == "change_level":
            print("Changing Security Level to", json_payload.get("level", "").lower())
            os.environ["SECURITY_LEVEL"] = json_payload.get("level", "").lower()
            print("Security Level (changed):", os.environ["SECURITY_LEVEL"])

        # Change the topic
        if json_payload.get("cmd", "").lower() == "change_topic":
            print("Changing Topic to", json_payload.get("topic", "").lower())
            os.environ["TOPIC"] = json_payload.get("topic", "").lower()
            print("Topic (changed):", os.environ["TOPIC"])

        if json_payload.get("cmd", "").lower() == "capture_photo":
            emp_id = int(json_payload.get("id"))
            print("Capturing images for emp_id", emp_id)

            try:
                '''
                Capture pincode and send it to the url endpoint along emp_id
                '''
                state = camera.capture_face_sending(emp_id)

                if state:
                    print("Faces stored successfully!")
                else:
                    print("Could not store faces")

            except Exception as e:
                print("Error:", e)

        # Capture and store a fingerprint
        if json_payload.get("cmd", "").lower() == "capture_finger":
            emp_id = int(json_payload.get("id"))
            print("Capturing fingerprints for emp_id", emp_id)

            try:
                state = fingerprint.enroll_print(emp_id)

                if state:
                    print("Fingerprint stored")
                    # To Do Send that fingerprint is stored into the backend
                else:
                    print("Fingerprint not stored")
            except Exception as e:
                print("Error:", e)

        if json_payload.get("cmd", "").lower() == "capture_pincode":
            emp_id = int(json_payload.get("id"))
            print("Capturing pincode for emp_id", emp_id)
            try:
                pincode = keypad.get_pin()
                url = 'http://localhost:'
                state = send_request.send_pincode(pincode, url)

                if state:
                    print("Pincode stored successfully!")
                else:
                    print("Could not store pincode")

            except Exception as e:
                print("Error:", e)
