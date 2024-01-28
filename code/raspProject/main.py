import json
import os
import random
import threading
import time
from paho.mqtt import client as mqtt_client
from configuration_mode import config_handler
from active_mode import main_loop
from dotenv import load_dotenv



broker = os.environ.get('BROKER')
port = os.environ.get('PORT')
topic = os.environ.get('TOPIC')
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
ca_cert = os.environ.get('CA')

# Event to control the read_input function
event = threading.Event()


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.tls_set(ca_certs="./mqtt_communication/emqxsl-ca.crt")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, int(port))
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global event

        payload = msg.payload.decode()
        print(f"Received `{payload}` from `{msg.topic}` topic")

        try:
            json_payload = json.loads(payload)

            if json_payload.get("mode", "").lower() == "configure":
                print("Configuration Mode Activated")
                event.clear()

                config_handler.json_handler(json_payload)

            elif json_payload.get("mode", "").lower() == "active":
                print("Active Mode Activated")
                event.set()

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    client.subscribe(topic)
    client.on_message = on_message


def read_input():
    while True:
        if event.is_set():
            main_loop.motion_detector()
        else:
            time.sleep(5)


def run():
    client = connect_mqtt()
    # Start a separate thread for MQTT client
    mqtt_thread = threading.Thread(target=client.loop_forever)
    subscribe(client)
    mqtt_thread.start()
    read_input()


if __name__ == '__main__':
    run()
