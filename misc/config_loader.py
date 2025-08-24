import configparser
import os


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser(interpolation=None)
        config_file = "config/config.ini"

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

    def get_mqtt_broker(self) -> str:
        return self.config["MQTT"]["broker"]

    def get_mqtt_username(self) -> str:
        return self.config["MQTT"]["username"]

    def get_mqtt_password(self) -> str:
        return self.config["MQTT"]["password"]

    def get_mqtt_topic_command(self) -> str:
        return self.config["MQTT"]["topic_command"]

    def get_mqtt_topic_state(self) -> str:
        return self.config["MQTT"]["topic_state"]

    def get_mqtt_topic_realtime_state(self) -> str:
        return self.config["MQTT"]["topic_realtime_state"]

    def get_coop_door_pins(self) -> dict[str, int]:
        return {
            "open": int(self.config["COOP_DOOR"]["open_pin"]),
            "close": int(self.config["COOP_DOOR"]["close_pin"]),
            "speed": int(self.config["COOP_DOOR"]["speed_pin"])
        }

    def get_coop_door_open_pin(self) -> int:
        return int(self.config["COOP_DOOR"]["open_pin"])

    def get_coop_door_close_pin(self) -> int:
        return int(self.config["COOP_DOOR"]["close_pin"])

    def get_coop_door_speed_pin(self) -> int:
        return int(self.config["COOP_DOOR"]["speed_pin"])

    def get_coop_door_logging(self) -> dict:
        return {
            "logfile": self.config["COOP_DOOR_LOGGING"]["logfile"],
            "level": self.config["COOP_DOOR_LOGGING"]["level"]
        }

    def get_coop_door_logging_logfile(self) -> str:
        return self.config["COOP_DOOR_LOGGING"]["logfile"]

    def get_coop_door_logging_level(self) -> str:
        return self.config["COOP_DOOR_LOGGING"]["level"]

    def get_coop_door_logging_message_format(self) -> str:
        return self.config["COOP_DOOR_LOGGING"]["message_format"]

    def get_coop_door_logging_date_time_format(self) -> str:
        return self.config["COOP_DOOR_LOGGING"]["date_time_format"]

    def get_coop_door_buttons_pins(self) -> dict[str, int]:
        return {
            "open": int(self.config["COOP_DOOR_BUTTONS"]["open_pin"]),
            "stop": int(self.config["COOP_DOOR_BUTTONS"]["stop_pin"]),
            "close": int(self.config["COOP_DOOR_BUTTONS"]["close_pin"])
        }

    def get_coop_door_buttons_open_pin(self) -> int:
        return int(self.config["COOP_DOOR_BUTTONS"]["open_pin"])

    def get_coop_door_buttons_stop_pin(self) -> int:
        return int(self.config["COOP_DOOR_BUTTONS"]["stop_pin"])

    def get_coop_door_buttons_close_pin(self) -> int:
        return int(self.config["COOP_DOOR_BUTTONS"]["close_pin"])

    def get_coop_door_buttons_logging(self) -> dict:
        return {
            "logfile": self.config["COOP_DOOR_BUTTONS_LOGGING"]["logfile"],
            "level": self.config["COOP_DOOR_BUTTONS_LOGGING"]["level"]
        }

    def get_coop_door_buttons_logging_logfile(self) -> str:
        return self.config["COOP_DOOR_BUTTONS_LOGGING"]["logfile"]

    def get_coop_door_buttons_logging_level(self) -> str:
        return self.config["COOP_DOOR_BUTTONS_LOGGING"]["level"]

    def get_coop_door_buttons_logging_message_format(self) -> str:
        return self.config["COOP_DOOR_BUTTONS_LOGGING"]["message_format"]

    def get_coop_door_buttons_logging_date_time_format(self) -> str:
        return self.config["COOP_DOOR_BUTTONS_LOGGING"]["date_time_format"]

    def get_coop_door_sensory_pins(self) -> dict[str, int]:
        return {
            "open": int(self.config["COOP_DOOR_SENSORS"]["open_pin"]),
            "close": int(self.config["COOP_DOOR_SENSORS"]["close_pin"])
        }

    def get_coop_door_sensors_open_pin(self) -> int:
        return int(self.config["COOP_DOOR_SENSORS"]["open_pin"])

    def get_coop_door_sensors_close_pin(self) -> int:
        return int(self.config["COOP_DOOR_SENSORS"]["close_pin"])

    def get_coop_door_sensors_logging(self) -> dict:
        return {
            "logfile": self.config["COOP_DOOR_SENSORS_LOGGING"]["logfile"],
            "level": self.config["COOP_DOOR_SENSORS_LOGGING"]["level"]
        }

    def get_coop_door_sensors_logging_logfile(self) -> str:
        return self.config["COOP_DOOR_SENSORS_LOGGING"]["logfile"]

    def get_coop_door_sensors_logging_level(self) -> str:
        return self.config["COOP_DOOR_SENSORS_LOGGING"]["level"]

    def get_coop_door_sensors_logging_message_format(self) -> str:
        return self.config["COOP_DOOR_SENSORS_LOGGING"]["message_format"]

    def get_coop_door_sensors_logging_date_time_format(self) -> str:
        return self.config["COOP_DOOR_SENSORS_LOGGING"]["date_time_format"]
