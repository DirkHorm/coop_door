#!/usr/bin/python
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------
# coop_door_sensors.py für den automatischen Start eingetragen in:
# Schauen, ob Script im Hintergrund läuft: ps aux | grep /home/pi/coop/coop_door_sensors.py
#
#
# CHANGELOG:
# 2024-08-11:
# Initiales Set-Up des Skripts
#--------------------------------------------------------------------------------

from gpiozero import Button
import paho.mqtt.client as mqtt
import logging
import logging.handlers
from enum import Enum, auto
from signal import pause
import threading

SENSOR_COOP_DOOR_OPENED_PIN = 26
SENSOR_COOP_DOOR_CLOSED_PIN = 19

# MQTT Broker (running on the OpenHAB Server)
BROKER_ADDRESS = 'house.lan'
MQTT_COOP_DOOR_SENSOR_TOPIC = 'garden/chickens/coopdoor/state'

CHECK_INTERVAL_WHEN_UNKNOWN = 10   # check all 10 seconds

last_state = None  # remember last state, so event is only published when it changed

class CoopDoorState(Enum):
    OPEN = auto()
    CLOSE = auto()
    UNKNOWN = auto()

def publish_coop_door_state(state):
    global last_state
    if state != last_state:                    
        state_name = state.name
        logging.info('Publishing state %s for coop door sensor' % state_name)
        client.publish(MQTT_COOP_DOOR_SENSOR_TOPIC, state_name)
    last_state = state

def setup_logging():
    log_handler = logging.handlers.WatchedFileHandler('/var/log/coop/coop_door_sensor.log')
    formatter = logging.Formatter('%(asctime)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

def evaluate_state():
    """Check sensors and publish current state (only if changed)"""
    if opened_sensor.is_pressed:
        publish_coop_door_state(CoopDoorState.OPEN)
    elif closed_sensor.is_pressed:
        publish_coop_door_state(CoopDoorState.CLOSE)
    else:
        publish_coop_door_state(CoopDoorState.UNKNOWN)

def periodic_check():
    """Run evaluate_state() periodically"""
    evaluate_state()
    threading.Timer(CHECK_INTERVAL, periodic_check).start()

# --- Main ---
setup_logging()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set('chicken', '0T"P0vy=`u.beNmUY^i.')
client.connect(BROKER_ADDRESS)
client.loop_start()

opened_sensor = Button(SENSOR_COOP_DOOR_OPENED_PIN, pull_up=True, bounce_time=0.1)
closed_sensor = Button(SENSOR_COOP_DOOR_CLOSED_PIN, pull_up=True, bounce_time=0.1)

opened_sensor.when_pressed = evaluate_state
closed_sensor.when_pressed = evaluate_state
opened_sensor.when_released = evaluate_state
closed_sensor.when_released = evaluate_state

evaluate_state()

periodic_check()

pause()

