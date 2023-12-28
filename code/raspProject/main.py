import subprocess
import random
import threading
import mqtt_communication.config_mqtt as config
from paho.mqtt import client as mqtt_client
from control_logic import json_decorder

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
        json_decorder.json_decorator(msg)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()