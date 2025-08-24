#!/usr/bin/python
# -*- coding: utf-8 -*-

from gpiozero import Button
from signal import pause
import paho.mqtt.client as mqtt
import logging
import logging.handlers
from enum import Enum, auto
import datetime as dt
import time

from misc.config_loader import Config
from misc.coop_door_state import CoopDoorState

cfg = Config()

UP_PIN = cfg.get_coop_door_buttons_open_pin()
STOP_PIN = cfg.get_coop_door_buttons_stop_pin()
DOWN_PIN = cfg.get_coop_door_buttons_close_pin()

BROKER_ADDRESS = cfg.get_mqtt_broker()
MQTT_COMMAND_TOPIC = cfg.get_mqtt_topic_command()

# Wartezeit für Entprellung in Sekunden
DEBOUNCE_DELAY = 0.05

client = None
up_button = None
stop_button = None
down_button = None

def coop_door_open():
    log(f'Button up pressed (confirmed)')
    current_date_and_time = dt.datetime.now()
    earliest_open_datetime = dt.datetime(
        current_date_and_time.year,
        current_date_and_time.month,
        current_date_and_time.day,
        7, 30, 0, 0
    )
    latest_open_datetime = dt.datetime(
        current_date_and_time.year,
        current_date_and_time.month,
        current_date_and_time.day,
        22, 0, 0, 0
    )

    if earliest_open_datetime < current_date_and_time < latest_open_datetime:
        publish_button_press(client, CoopDoorState.OPEN)
    else:
        log(f'Prevented coop door from opening at {current_date_and_time}')


def coop_door_stop():
    log(f'Button stop pressed (confirmed)')
    publish_button_press(client, CoopDoorState.STOP)


def coop_door_close():
    log(f'Button down pressed (confirmed)')
    publish_button_press(client, CoopDoorState.CLOSE)


# Hilfsfunktion: Button-Entprellung
def handle_button(button, action_fn):
    time.sleep(DEBOUNCE_DELAY)
    if button.is_pressed:  # nur wenn nach Delay noch gedrückt
        action_fn()


def publish_button_press(client, button_action):
    button_action_name = button_action.name
    log(f'Publishing coop door button move {button_action_name}')
    client.publish(MQTT_COMMAND_TOPIC, button_action_name)
    log(f'Published coop door button move {button_action_name}')


def on_connect(client, userdata, flags, result_code, properties):
    if result_code == 0:
        client.subscribe(MQTT_COMMAND_TOPIC)
        log(f'Connected to mqtt broker and topic {MQTT_COMMAND_TOPIC}')
    else:
        log(f'Mqtt Broker connection failed with error code {result_code}')


def setup_logging():
    log_handler = logging.handlers.WatchedFileHandler(cfg.get_coop_door_buttons_logging_logfile())
    formatter = logging.Formatter(
        cfg.get_coop_door_logging_message_format(),
        cfg.get_coop_door_buttons_logging_date_time_format()
    )
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(cfg.get_coop_door_buttons_logging_level())


def log(message: str, *args, level: int = logging.INFO, exc=None) -> None:
    if exc:
        logging.log(level, message, *args, exc_info=exc)
    else:
        logging.log(level, message, *args)

def init_buttons():
    global up_button, stop_button, down_button
    up_button = Button(UP_PIN, pull_up=True)
    stop_button = Button(STOP_PIN, pull_up=True)
    down_button = Button(DOWN_PIN, pull_up=True)

def main():
    global client
    setup_logging()
    try:
        init_buttons()

        log('Connecting to mqtt')
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        log('Mqtt client created')
        client.username_pw_set(cfg.get_mqtt_username(), cfg.get_mqtt_password())
        log('Mqtt username and password set')
        client.on_connect = on_connect
        log('Trying to connect to Mqtt server')
        client.connect(BROKER_ADDRESS)
        log('Connected to Mqtt server')
        client.loop_start()

        log('Waiting for button event')
        stop_button.when_pressed = lambda: handle_button(stop_button, coop_door_stop)
        up_button.when_pressed = lambda: handle_button(up_button, coop_door_open)
        down_button.when_pressed = lambda: handle_button(down_button, coop_door_close)

        pause()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        log('coop_door_buttons.py broke with exception', level=logging.ERROR, exc=err)
    finally:
        if client:
            client.unsubscribe(MQTT_COMMAND_TOPIC)
            client.disconnect()
        log('Finishing coop door buttons script')

if __name__ == '__main__':
    main()