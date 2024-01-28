import random
import time
from paho.mqtt import client as mqtt_client
import json
import os


broker = os.environ.get('BROKER')
port = os.environ.get('PORT')
topic = os.environ.get('TOPIC')
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

script_dir = os.path.dirname(os.path.realpath(__file__))
cert_path = os.path.join(script_dir, 'emqxsl-ca.crt')


def connect_mqtt():
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


def publish(client, json_data):
    try:
        msg = str(json_data)
        result = client.publish(topic, msg)
        status = result.rc
        if status == mqtt_client.MQTT_ERR_SUCCESS:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}. Result code: {status}")
    except Exception as e:
        print(f"Error publishing message: {e}")


def run(data):
    json_data = json.dumps(data)
    client = connect_mqtt()
    client.loop_start()
    while not client.is_connected():
        time.sleep(1)
    client.publish(topic, json_data)
    time.sleep(1)
    client.disconnect()