import json
import subprocess


script_path_encode = "face_detection/encode_faces.py"
script_path_recognize = "face_detection/recognize_faces_image.py"

dataset_path = "face_detection/datasets"

recognize_path = "face_detection/captured/001.jpg"
encodings_path = "face_detection/encodings.pickle"
detection_method = "hog"  # or "hog"

encoding_command = [
    "python3",
    script_path_encode,
    "-i", dataset_path,
    "-e", encodings_path,
    "-d", detection_method
]

recognize_command = [
    "python3",
    script_path_recognize,
    "-e", encodings_path,
    "-i", recognize_path,
    "-d", detection_method
]


def encode_faces():
    subprocess.call(encoding_command)


def recognize_faces():
    output = subprocess.check_output(recognize_command, text=True)
    try:
        result = json.loads(output)
        recognized_name = result.get("Recognized")
        if recognized_name:
            print(f"Recognized face name: {recognized_name}")
            return recognized_name
        else:
            print("No face recognized.")
            return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON output: {e}")
        print("Recognition may have failed.")