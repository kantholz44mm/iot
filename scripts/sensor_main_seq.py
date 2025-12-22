#!/usr/bin/python3
from gpiozero import DistanceSensor, MotionSensor, Button
from signal import pause
import time
from datetime import datetime
import json
from time import sleep

import paho.mqtt.client as mqtt

import api
from pathlib import Path
from datetime import datetime, timedelta

def on_connect(client, userdata, flags, rc):
    """Wird aufgerufen, wenn der Client eine Verbindung zum Broker herstellt."""
    if rc == 0:
        print("Verbunden mit MQTT Broker.")
    else:
        print(f"Verbindung fehlgeschlagen, Return Code {rc}")

def publish(client,sensor, value_sensor, timestamp_sensor, topic):
   
    msg = json.dumps({"Sensor" : sensor, "Value" : value_sensor, "Time" : timestamp_sensor })
    #msg = f"{sensor} : {message}"
    result = client.publish(topic, msg)
    status = result[0]
    
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def publish_all(client, topic):
    dst_ultra = str(u_sonic_sensor.distance)
    timestamp_sensor = str(datetime.now())
    data = {"Sensor_PIR" : pir_detect, "Sensor_Ultra" : dst_ultra, "Sensor_Sound" : sound_detect, "Time" : timestamp_sensor}
    
    #msg = f"{sensor} : {message}"

    api.push_data(data)

    global enough_data
    if (enough_data > 30):
        data["Prediction"] = api.estimate_current_state()
        data["Anomaly"] = api.detect_anomalies(0.7, timedelta(days=3))
        print(f"Data prediction is: {data["Prediction"]} and Anomaly testing is: {data["Anomaly"]}")
    else:
        data["Prediction"] = ["Waiting for enought samples ...", 0]
        data["Anomaly"] = "Waiting for enought samples ..."
        enough_data += 1
    msg = json.dumps(data)

    result = client.publish(topic, msg)
    status = result[0]
    
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")   
    else:
        print(f"Failed to send message to topic {topic}")


def set_pir():
    global pir_detect
    print("Pir detected")
    pir_detect = 1

def set_sound():
    global sound_detect
    sound_detect = 1

def set_ultra():
    ultra_dist = str(u_sonic_sensor.distance)

def reset_vals():
    global pir_detect
    global sound_detect
    pir_detect = 0
    sound_detect = 0
    

audio_sensor = Button(22, pull_up=None, active_state=False)
motion_sensor = Button(27, pull_up=None, active_state=False)
u_sonic_sensor = DistanceSensor(18, 17, max_distance=2, threshold_distance=0.5)

broker = 'broker.hivemq.com'
port = 1883
topic = "iot/sensors"
client_id = f'python-mqtt-55323'

pir_detect = 0
sound_detect = 0
client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.connect(broker, port)

audio_sensor.when_pressed = set_sound
motion_sensor.when_pressed = set_pir

api.load_model()
enough_data = 0

client.loop_start()

try:
    while True:
        publish_all(client, topic)
        reset_vals()
        sleep(0.5)
finally:

    client.loop_stop()
    client.disconnect()
    print("Verbindung getrennt.")

