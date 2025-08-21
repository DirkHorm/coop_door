import configparser
import os

class Config:
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file {config_file} not found")
        
        self.config.read(config_file)

    def get_mqtt_config(self):
        return {
            "broker": self.config["MQTT"]["broker"],
            "username": self.config["MQTT"]["username"],
            "password": self.config["MQTT"]["password"],
            "topic_command": self.config["MQTT"]["topic_command"],
            "topic_state": self.config["MQTT"]["topic_state"]
        }

    def get_mqtt_broker(self):
        return self.config["MQTT"]["broker"]

    def get_mqtt_username(self):
        return self.config["MQTT"]["username"]

    def get_mqtt_password(self):
        return self.config["MQTT"]["password"]

    def get_mqtt_topic_command(self):
        return self.config["MQTT"]["topic_command"]

    def get_mqtt_topic_state(self):
        return self.config["MQTT"]["topic_state"]

    def get_coop_door_pins(self):
        return {
            "open": self.config["COOP_DOOR"]["open_pin"],
            "close": self.config["COOP_DOOR"]["close_pin"],
            "speed": self.config["COOP_DOOR"]["speed_pin"]
        }

    def get_coop_door_open_pin(self):
            return self.config["COOP_DOOR"]["open_pin"]

    def get_coop_door_close_pin(self):
            return self.config["COOP_DOOR"]["close_pin"]

    def get_coop_door_speed_pin(self):
            return self.config["COOP_DOOR"]["speed_pin"]

    def get_coop_door_logging(self):
        return {
            "logfile": self.config["COOP_DOOR_LOGGING"]["logfile"],
            "level": self.config["COOP_DOOR_LOGGING"]["level"]
        }

    def get_coop_door_logging_logfile(self):
        return self.config["COOP_DOOR_LOGGING"]["logfile"],

    def get_coop_door_logging_level(self):
        return self.config["COOP_DOOR_LOGGING"]["level"]

    def get_coop_door_buttons_pins(self):
        return {
            "open": self.config["COOP_DOOR_BUTTONS"]["open_btn_pin"],
            "stop": self.config["COOP_DOOR_BUTTONS"]["stop_btn_pin"],
            "close": self.config["COOP_DOOR_BUTTONS"]["close_btn_pin"]
        }

    def get_coop_door_buttons_open_pin(self):
        return self.config["COOP_DOOR_BUTTONS"]["open_pin"]

    def get_coop_door_buttons_stop_pin(self):
        return self.config["COOP_DOOR_BUTTONS"]["stop_pin"]

    def get_coop_door_buttons_close_pin(self):
        return self.config["COOP_DOOR_BUTTONS"]["close_pin"]

    def get_coop_door_buttons_logging(self):
        return {
            "logfile": self.config["COOP_DOOR_BUTTONS_LOGGING"]["logfile"],
            "level": self.config["COOP_DOOR_BUTTONS_LOGGING"]["level"]
        }

    def get_coop_door_buttons_logging_logfile(self):
        return self.config["COOP_DOOR_BUTTONS_LOGGING"]["logfile"],

    def get_coop_door_buttons_logging_level(self):
        return self.config["COOP_DOOR_BUTTONS_LOGGING"]["level"]
