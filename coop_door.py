#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------
# coop_door.py für den automatischen Start eingetragen als Service: 
# Content in Service:
# [Unit]
# Description=Coop Door Control Service
# After=network.target
# Wants=network-online.target
# 
# [ Service]
# ExecStart=/bin/bash -c 'source /pyVEnv/coop/bin/activate && /pyVEnv/coop/bin/python /home/dirk/coop/coop_door.py'
# WorkingDirectory=/home/dirk/coop
# Restart=always
# User=root
# Group=root
# Environment="PYTHONUNBUFFERED=1"
# StandardOutput=syslog
# StandardError=syslog
# 
# [Install]
# WantedBy=multi-user.target
# 
# Run the service automatically:
# Systemd neu laden, damit die neue Service-Datei erkannt wird
# sudo systemctl daemon-reload  
# 
# Dienst starten
# sudo systemctl start coop_door  
# 
# Status des Dienstes prüfen
# sudo systemctl status coop_door  
# 
# Dienst für den Autostart aktivieren
# sudo systemctl enable coop_door
# --------------------------------------------------------------------------------

import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
import logging
import logging.handlers

from misc.config_loader import Config
from misc.coop_door_state import CoopDoorState

cfg = Config()

COOP_DOOR_OPEN_PIN = cfg.get_coop_door_open_pin()
COOP_DOOR_CLOSE_PIN = cfg.get_coop_door_close_pin()
COOP_DOOR_SPEED_PIN = cfg.get_coop_door_speed_pin()

MQTT_COMMAND_TOPIC = cfg.get_mqtt_topic_command()
MQTT_COOP_DOOR_STATE_TOPIC = cfg.get_mqtt_topic_state()

DUTY_CYCLE_MIN = 0
# 100% performance, so the full power goes to the motor. At 12 V with 75% it would only be 9 V given to the motor, e.g.;
# to be tried out, if 75% would also be enough!
DUTY_CYCLE_MAX = 100

pwm_speed = None


def reset_pins():
    log('Resetting pins to original state')
    gpio.output(COOP_DOOR_OPEN_PIN, gpio.LOW)
    gpio.output(COOP_DOOR_CLOSE_PIN, gpio.LOW)
    pwm_speed.ChangeDutyCycle(DUTY_CYCLE_MIN)  # stop motor
    log('Reset pins to original state')


def move_door(pin, position):
    reset_pins()
    pwm_speed.ChangeDutyCycle(DUTY_CYCLE_MAX)
    log('Setting pin %d to HIGH for %s coop door' % (pin, position))
    gpio.output(pin, gpio.HIGH)
    log('Set pin %d to HIGH' % pin)


def stop_door_move():
    log('Stopping coop door move')
    reset_pins()
    log('Stopped coop door move')


def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    log('Message received from topic "%s" with payload "%s"' % (topic, payload))

    if topic == MQTT_COOP_DOOR_STATE_TOPIC:
        reset_pins()
        log('Pins for Coop Door reset')
    elif topic == MQTT_COMMAND_TOPIC:
        command = payload
        log('Received command "%s" from broker' % command)
        if CoopDoorState.OPEN.name == command:
            log('In OPEN')
            move_door(COOP_DOOR_OPEN_PIN, 'opening')
        elif CoopDoorState.CLOSE.name == command:
            log('In CLOSE')
            move_door(COOP_DOOR_CLOSE_PIN, 'closing')
        elif CoopDoorState.STOP.name == command:
            stop_door_move()


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(MQTT_COMMAND_TOPIC)
    # client.subscribe(MQTT_COOP_DOOR_STATE_TOPIC)
    log('Connected to mqtt broker and topic %s' % MQTT_COMMAND_TOPIC)


def setup_logging():
    log_handler = logging.handlers.WatchedFileHandler(cfg.get_coop_door_logging_logfile())
    formatter = logging.Formatter(
        cfg.get_coop_door_logging_message_format(),
        cfg.get_coop_door_logging_date_time_format()
    )
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(cfg.get_coop_door_logging_level())


def log(message: str, *args, level: int = logging.INFO, exc=None) -> None:
    if exc:
        logging.log(level, message, *args, exc_info=exc)
    else:
        logging.log(level, message, *args)


def init_pins():
    global pwm_speed
    gpio.setmode(gpio.BCM)
    gpio.setup([COOP_DOOR_OPEN_PIN, COOP_DOOR_CLOSE_PIN], gpio.OUT, initial=gpio.LOW)
    gpio.setup(COOP_DOOR_SPEED_PIN, gpio.OUT)

    pwm_speed = gpio.PWM(COOP_DOOR_SPEED_PIN, DUTY_CYCLE_MAX)  # 100 Hz
    pwm_speed.start(DUTY_CYCLE_MIN)  # start with switched off motor (= 0%)


def main():
    setup_logging()
    client = None
    try:
        init_pins()

        log('Connecting to mqtt')
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        log('Mqtt client created')
        client.username_pw_set(cfg.get_mqtt_username(), cfg.get_mqtt_password())
        log('Mqtt username and password set')
        client.on_connect = on_connect
        client.on_message = on_message
        log('Trying to connect to Mqtt server')
        client.connect(cfg.get_mqtt_broker())
        log('Connected to Mqtt server')
        client.loop_forever(retry_first_connection=False)
    except KeyboardInterrupt:
        pass
    except Exception as err:
        pass
        log('coop_door.py broke with exception', level=logging.ERROR, exc=err)
    finally:
        if client:
            client.loop_stop()
            client.unsubscribe(MQTT_COMMAND_TOPIC)
            client.unsubscribe(MQTT_COOP_DOOR_STATE_TOPIC)
            client.disconnect()
        gpio.cleanup()  # this ensures a clean exit
        log('Finishing coop door script')


if __name__ == '__main__':
    main()

