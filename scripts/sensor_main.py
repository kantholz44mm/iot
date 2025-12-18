#!/usr/bin/python3
from gpiozero import DistanceSensor, MotionSensor, Button
from signal import pause
import time
from datetime import datetime
import json

import paho.mqtt.client as mqtt

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

def publish_audio_detected():
    publish(client, "Audio Sensor", 1, str(datetime.now()), topic)

def publish_motion_detected():
    publish(client, "PIR Sensor", 1, str(datetime.now()), topic)
    #opt ultrasonic distance send

def publish_distance_in_range():
    publish(client, "Ultrasonic Sensor", str(u_sonic_sensor.distance), str(datetime.now()), topic)


audio_sensor = Button(22, pull_up=None, active_state=False)
motion_sensor = Button(27, pull_up=None, active_state=False)
u_sonic_sensor = DistanceSensor(18, 17, max_distance=2, threshold_distance=0.5)

broker = 'broker.hivemq.com'
port = 1883
topic = "iot/sensors"
client_id = f'python-mqtt-55323'


client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.connect(broker, port)

audio_sensor.when_pressed = publish_audio_detected
motion_sensor.when_pressed = publish_motion_detected
u_sonic_sensor.when_in_range = publish_distance_in_range



client.loop_start()

try:
    pause()
finally:

    client.loop_stop()
    client.disconnect()
    print("Verbindung getrennt.")


#TODO: PIR Sensor als genauere Aktivierung für Ultrasonic, um dann dort distance auszulesen.
#Objekte, welche immer im schwellwert sitzen blockieren die in range methode. vielleicht flag setzen, wenn in range und out of range
