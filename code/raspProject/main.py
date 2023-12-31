import json
import subprocess
import random
import threading
import time

import mqtt_communication.config_mqtt as config
from paho.mqtt import client as mqtt_client
from control_logic import json_decorder
from attendance_recognition import main_loop

broker = config.broker
port = config.port
topic = config.topic
# generate client ID with pub prefix randomly
client_id_sub = f'python-mqtt-{random.randint(0, 100)}'
username = config.username
password = config.password

# Event to control the read_input function
event = threading.Event()


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
        global event  # Use the global event

        payload = msg.payload.decode()
        print(f"Received `{payload}` from `{msg.topic}` topic")

        json_payload = json.loads(payload)

        if json_payload.get("mode", "").lower() == "configure":
            print("Configuration Mode Activated")
            json_decorder.json_decorator(msg)
            # Stop reading input in configure mode
            event.clear()

        elif json_payload.get("mode", "").lower() == "active":
            print("Active Mode Activated")
            # Start reading input in active mode
            event.set()

        elif json_payload.get("mode", "").lower() == "unlock":
            print("Unlock the Door")

    client.subscribe(topic)
    client.on_message = on_message


def read_input():
    while True:
        if event.is_set():
            main_loop.motion_detector()
        else:
            time.sleep(1)


def run():
    client = connect_mqtt()
    # Start a separate thread for MQTT client
    mqtt_thread = threading.Thread(target=client.loop_forever)
    subscribe(client)
    mqtt_thread.start()
    read_input()


if __name__ == '__main__':
    run()
