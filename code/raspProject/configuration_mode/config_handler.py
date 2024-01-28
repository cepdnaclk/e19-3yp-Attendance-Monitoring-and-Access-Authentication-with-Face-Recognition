import json
import os
from mqtt_communication import publish_msg
from components import fingerprint, camera, keypad, doorlock
from configuration_mode import send_request
from dotenv import load_dotenv, set_key

# Adjust the path to point to the root folder
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

security_level = os.environ.get('SECURITY_LEVEL')


def json_handler(json_payload,queue):
    # `json_payload` is a Python dictionary containing the parsed JSON data
    # You can access values using keys, e.g., json_payload["key"]

    if json_payload.get("mode", "").lower() == "configure":

        # Change the security level
        if json_payload.get("cmd", "").lower() == "change_level":
            print("Changing Security Level to", json_payload.get("level", "").lower())
            modified_value = json_payload.get("level", "").lower()
            set_key('.env', 'SECURITY_LEVEL', modified_value)            
            queue.put(f'Changing Security Level to level {security_level}')

        # Change the topic
        if json_payload.get("cmd", "").lower() == "change_topic":
            print("Changing Topic to", json_payload.get("topic", "").lower())
            modified_value = json_payload.get("topic", "").lower()
            set_key('.env', 'TOPIC', modified_value) 
            queue.put(f'Topic changed {modified_value}')
        
        if json_payload.get("cmd", "").lower() == "unlock_door":
            print("Unlocking the Door!")
            queue.put('Unlocking the Door!')
            doorlock.open_lock(queue)

        
        # Capture photos
        if json_payload.get("cmd", "").lower() == "capture_photo":
            emp_id = int(json_payload.get("emp_id"))
            print("Capturing images for emp_id", emp_id)
            queue.put(f'Capturing images for {emp_id}')

            try:
                '''
                Capture pincode and send it to the url endpoint along emp_id
                '''
                state = camera.capture_face_sending(emp_id)

                if state:
                    print("Faces stored successfully!")
                    queue.put('Faces stored successfully!')
                else:
                    print("Could not store faces")
                    queue.put('Could not store faces')

            except Exception as e:
                print("Error:", e)

        # Capture and store a fingerprint
        if json_payload.get("cmd", "").lower() == "capture_finger":
            emp_id = int(json_payload.get("emp_id"))
            print("Capturing fingerprints for emp_id", emp_id)
            queue.put('Capturing fingerprints for {emp_id}')

            try:
                state = fingerprint.enroll_print(emp_id)

                if state:
                    print("Fingerprint stored")
                    queue.put('Fingerprint stored')
                    # To Do Send that fingerprint is stored into the backend
                else:
                    print("Unable to store the fingerprint")
                    queue.put('Unable to store the fingerprint')
            except Exception as e:
                print("Error:", e)

        if json_payload.get("cmd", "").lower() == "capture_pincode":
            emp_id = int(json_payload.get("emp_id"))
            print("Capturing pincode for emp_id", emp_id)
            queue.put('Capturing pincode for {emp_id}')
            try:
                pincode = keypad.get_pin()
                url = 'https://facesecure.azurewebsites.net/attendanceManagement/save-pin/'
                state = send_request.send_pincode(pincode, url, emp_id)

                if state:
                    print("Pincode stored successfully!")
                    queue.put('Pincode stored successfully!')
                else:
                    print("Could not store pincode")
                    queue.put('Could not store pincode')

            except Exception as e:
                print("Error:", e)
