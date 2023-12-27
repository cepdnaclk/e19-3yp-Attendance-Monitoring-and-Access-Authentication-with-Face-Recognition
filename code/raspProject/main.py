import subprocess
import random
import threading

import mqtt_communication.config as config
from paho.mqtt import client as mqtt_client

script_path_encode = "face_recognition/encode_faces.py"
script_path_recognize = "face_recognition/recognize_faces_image.py"

dataset_path = "face_recognition/datasets"

recognize_path = "face_recognition/captured/001.jpeg"
encodings_path = "face_recognition/encodings.pickle"
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

broker = config.broker
port = config.port
topic = config.topic
# generate client ID with pub prefix randomly
client_id_sub = f'python-mqtt-{random.randint(0, 100)}'
username = config.username
password = config.password


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id_sub)
    client.tls_set(ca_certs="./mqtt_communication/emqxsl-ca.crt")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Received `{payload}` from `{msg.topic}` topic")
        if msg.topic == topic and payload.lower() == "update_device":
            print("Running Device Database Update...")
            #subprocess.run(encoding_command)
            threading.Thread(target=subprocess.run, args=(encoding_command,)).start()

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()