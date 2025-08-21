#!/usr/bin/python
# -*- coding: utf-8 -*-

from gpiozero import Button
from signal import pause
import paho.mqtt.client as mqtt
import logging
import logging.handlers
from enum import Enum, auto
import datetime as dt
from misc.config_loader import Config

cfg = Config("/home/pi/coop/config.ini")
mqtt_config = cfg.get_mqtt()

# MQTT-Client einrichten
client = mqtt.Client()
client.username_pw_set(mqtt_config["username"], mqtt_config["password"])
client.connect(mqtt_config["broker"], mqtt_config["port"])

UP_PIN = 13
STOP_PIN = 6
DOWN_PIN = 5 

BROKER_ADDRESS = 'house.lan'
MQTT_COMMAND_TOPIC = 'garden/chickens/coopdoor'

class CoopDoorButtonAction(Enum):
    OPEN = auto()
    CLOSE = auto()
    STOP = auto()

def coop_door_open():
    log(f'Button up pressed')
    current_date_and_time = dt.datetime.now()
    # Prevent the coop door being manually opened before or after a special datetime
    earliest_open_datetime = dt.datetime(int(current_date_and_time.strftime('%Y')), int(current_date_and_time.strftime('%m')), int(current_date_and_time.strftime('%d')), 7, 30, 0, 0)
    latest_open_datetime = dt.datetime(int(current_date_and_time.strftime('%Y')), int(current_date_and_time.strftime('%m')), int(current_date_and_time.strftime('%d')), 22, 0, 0, 0)

    if current_date_and_time > earliest_open_datetime and current_date_and_time < latest_open_datetime:
        publish_button_press(client, CoopDoorButtonAction.OPEN)
    else:
        log(f'Prevented coop door from opening at {current_date_and_time}')

def coop_door_stop():
    log(f'Button stop pressed')
    publish_button_press(client, CoopDoorButtonAction.STOP)

def coop_door_close():
    log(f'Button down pressed')
    publish_button_press(client, CoopDoorButtonAction.CLOSE)

    
def publish_button_press(client, button_action):
    button_action_name = button_action.name
    log(f'Publishing coop door button move {button_action_name}')
    client.publish(MQTT_COMMAND_TOPIC, button_action_name)
    log(f'Published coop door button move {button_action_name}')
    
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        client.subscribe(MQTT_COMMAND_TOPIC)
        log(f'Connected to mqtt broker and topic {MQTT_COMMAND_TOPIC}')
    else:
        log(f'Mqtt Broker connection failed with the following error code {reason_code}')
    
def setup_logging():
    log_handler = logging.handlers.WatchedFileHandler('/var/log/coop/coop_door_buttons.log')
    formatter = logging.Formatter(
        '%(asctime)s: %(message)s',
        "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

def log(message: str, *args, level: int = logging.INFO) -> None:
    if args:
        logging.log(level, message, args)
    else:
        logging.log(level, message)

client = None
try:
    setup_logging()

    # pull_up und bounce_time haben das Problem mit den "Geisterklicks" nicht gelöst, sondern verhindert, dass die Taster überhaupt greifen
    up_button = Button(UP_PIN, pull_up=True, bounce_time=0.1) 
    stop_button = Button(STOP_PIN, pull_up=True, bounce_time=0.1)
    down_button = Button(DOWN_PIN, pull_up=True, bounce_time=0.1)

    log('Connecting to mqtt')
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    log('Mqtt client created')
    client.username_pw_set('chicken', '0T"P0vy=`u.beNmUY^i.')
    log('Mqtt username and password set')
    client.on_connect = on_connect
    log('Trying to connect to Mqtt server')
    client.connect(BROKER_ADDRESS)
    log('Connected to Mqtt server')
    client.loop_start()
    
    log('Waiting for button event')
    stop_button.when_pressed = coop_door_stop
    up_button.when_pressed = coop_door_open
    down_button.when_pressed = coop_door_close

    pause()
except KeyboardInterrupt:
    pass
except Exception as err:
    pass
    log('coop_door_buttons.py broke with exception', err, logging.ERROR)
finally:
    if client:
        client.unsubscribe(MQTT_COMMAND_TOPIC)
        client.disconnect()
    log('Finishing coop door buttons script')



