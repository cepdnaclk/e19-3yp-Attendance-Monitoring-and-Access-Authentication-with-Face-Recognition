import json
import os
import random
import threading
import time
from paho.mqtt import client as mqtt_client
import RPi.GPIO as GPIO

from configuration_mode import config_handler
from active_mode import main_loop
from dotenv import load_dotenv
from gui import run_gui
from queue import Queue
GPIO.setup(19,GPIO.OUT)

load_dotenv()

broker = os.getenv('BROKER')
port = os.getenv('PORT')
topic = os.getenv('TOPIC')
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
ca_cert = os.getenv('CA')

# Event to control the read_input function
event = threading.Event()

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.tls_set(ca_certs="./mqtt_communication/emqxsl-ca.crt")
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, int(port))
    return client

def subscribe(client: mqtt_client,queue):
    def on_message(client, userdata, msg):
        global event
        global security_level
        
        payload = msg.payload.decode()
        print(f"Received `{payload}` from `{msg.topic}` topic")

        try:
            json_payload = json.loads(payload)
            if json_payload.get("mode", "").lower() == "configure":
                print("Configuration Mode Activated")
                event.clear()
                config_handler.json_handler(json_payload,queue)
            elif json_payload.get("mode", "").lower() == "active":
                print("Active Mode Activated")
                security_level = json_payload.get("level", "").lower()
                event.set()
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        
        # Put the payload in the queue for further processing
        

    client.subscribe(topic)
    client.on_message = on_message

def read_input(queue: Queue):
    GPIO.output(19,1)
    global security_level
    while True:
        # Check the queue for messages from MQTT
        while not queue.empty():
            message = queue.get()
            print(f"Processing message from MQTT: {message}")

        if event.is_set():
            main_loop.motion_detector(queue)
        else:
            time.sleep(5)

def run():
    queue = Queue()
    client = connect_mqtt()
    # Start a separate thread for MQTT client
    mqtt_thread = threading.Thread(target=client.loop_forever)
    gui_thread = threading.Thread(target=run_gui, args=(queue,))
    subscribe(client,queue)
    mqtt_thread.start()
    gui_thread.start()
    read_input(queue)

if __name__ == '__main__':
    run()
