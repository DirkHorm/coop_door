#!/usr/bin/python
# -*- coding: utf-8 -*-

from gpiozero import Button
from signal import pause
import paho.mqtt.client as mqtt
import logging
import logging.handlers

from misc.config_loader import Config
from misc.coop_door_state import CoopDoorState

cfg = Config()

# Initializing pins
SENSOR_COOP_DOOR_OPENED_PIN = cfg.get_coop_door_sensors_open_pin()
SENSOR_COOP_DOOR_CLOSED_PIN = cfg.get_coop_door_sensors_close_pin()

MQTT_COOP_DOOR_STATE_TOPIC = cfg.get_mqtt_topic_state()
MQTT_COOP_DOOR_REALTIME_STATE_TOPIC = cfg.get_mqtt_topic_realtime_state()

SENSOR_BOUNCE_TIME = 0.3

# Global last state to only publish a state, when it changed
last_state = None

client = None
door_open_sensor = None
door_closed_sensor = None


def setup_logging():
    log_handler = logging.handlers.WatchedFileHandler(cfg.get_coop_door_sensors_logging_logfile())
    formatter = logging.Formatter(
        cfg.get_coop_door_sensors_logging_message_format(),
        cfg.get_coop_door_sensors_logging_date_time_format()
    )
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(cfg.get_coop_door_sensors_logging_level())


def log(message: str, *args, level: int = logging.INFO, exc=None) -> None:
    if exc:
        logging.log(level, message, *args, exc_info=exc)
    else:
        logging.log(level, message, *args)

def publish_state(new_state):
    global last_state
    log(f'Current realtime state {last_state}, new state {new_state}')
    # only publish when state changed
    if new_state != last_state:
        log(f'Realtime state changed from {last_state} to {new_state}')
        realtime_state_info = client.publish(MQTT_COOP_DOOR_REALTIME_STATE_TOPIC, new_state)
        log(f'Published realtime state {new_state} to topic {MQTT_COOP_DOOR_REALTIME_STATE_TOPIC} with rc {realtime_state_info.rc}')

        # Only open and closed are published to the state topic which can be used to set a switch in OpenHab, e.g.
        if new_state in [CoopDoorState.OPEN.name, CoopDoorState.CLOSED.name]:
            state_info = client.publish(MQTT_COOP_DOOR_STATE_TOPIC, new_state, retain=True)
            log(f'Published state {new_state} to topic {MQTT_COOP_DOOR_STATE_TOPIC} with rc {state_info.rc}')

        last_state = new_state

def door_opened():
    publish_state(CoopDoorState.OPEN.name)

def door_closed():
    publish_state(CoopDoorState.CLOSED.name)

# For the time the door is opening or closing, the state is "unknown"
def door_running():
    publish_state(CoopDoorState.RUNNING.name)


def on_connect(client, userdata, flags, result_code, properties):
    log(f"Connected with result code {result_code}")


def init_sensors():
    global door_open_sensor, door_closed_sensor
    # Initialize sensors
    door_open_sensor = Button(SENSOR_COOP_DOOR_OPENED_PIN, pull_up=True, bounce_time=SENSOR_BOUNCE_TIME)
    door_closed_sensor = Button(SENSOR_COOP_DOOR_CLOSED_PIN, pull_up=True, bounce_time=SENSOR_BOUNCE_TIME)


def main():
    global client
    setup_logging()
    try:
        init_sensors()

        log('Connecting to mqtt')
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        log('Mqtt client created')
        client.username_pw_set(cfg.get_mqtt_username(), cfg.get_mqtt_password())
        log('Mqtt username and password set')
        log('Trying to connect to Mqtt server')
        client.on_connect = on_connect
        client.connect(cfg.get_mqtt_broker())
        log('Connected to Mqtt server')
        client.loop_start()

        # Waiting for event to publish the current state
        door_open_sensor.when_pressed = door_opened
        door_closed_sensor.when_pressed = door_closed

        # For the time opening or closing, when no sensor is active
        door_open_sensor.when_released = door_running
        door_closed_sensor.when_released = door_running

        pause()
    except KeyboardInterrupt:
        log("coop_door.py interrupted by user", level=logging.WARNING)
    except Exception as err:
        log("coop_door.py broke with exception", level=logging.ERROR, exc=err)
    finally:
        if client:
            client.loop_stop()
            client.disconnect()
        log('Finishing coop door sensors script')


if __name__ == '__main__':
    main()
