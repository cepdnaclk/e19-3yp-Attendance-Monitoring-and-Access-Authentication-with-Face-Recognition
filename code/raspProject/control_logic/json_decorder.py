import json
from control_logic import cmd_scripts
import os
from config_logic import make_folder


def json_decorator(msg):
    payload = msg.payload.decode()
    try:
        json_payload = json.loads(payload)
        # Now `json_payload` is a Python dictionary containing the parsed JSON data
        # You can access values using keys, e.g., json_payload["key"]

        if json_payload.get("mode","").lower() == "configure":
            print("Configuration Mode Activated")

            if json_payload.get("cmd", "").lower() == "change_level":
                print("Changing Security Level to", json_payload.get("sl","").lower())
                os.environ["SECURITY_LEVEL"] = json_payload.get("sl","").lower()
                # print("Security Level (changed):", os.environ["SECURITY_LEVEL"])

            if json_payload.get("cmd", "").lower() == "update_device":
                print("Running Device Database Update...")
                cmd_scripts.encode_faces()
                # threading.Thread(target=subprocess.run, args=(encoding_command,)).start()

            if json_payload.get("cmd", "").lower() == "capture_image":
                print("Getting Ready for capturing images...")
                print("Making folder...", json_payload.get("name","").lower())
                make_folder.create_folder(json_payload.get("name","").lower())

            if json_payload.get("cmd", "").lower() == "capture_fp":
                print("Getting Ready for capturing finger print...")

            if json_payload.get("cmd", "").lower() == "capture_pin":
                print("Getting Ready for capturing PIN...")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")