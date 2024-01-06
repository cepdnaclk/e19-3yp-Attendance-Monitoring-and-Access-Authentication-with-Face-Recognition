import subprocess


script_path_encode = "face_detection/encode_faces.py"
script_path_recognize = "face_detection/recognize_faces_image.py"

dataset_path = "face_detection/datasets"

recognize_path = "face_detection/captured/001.jpeg"
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
    subprocess.call(recognize_command)