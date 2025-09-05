# Coop Door Control

The *coop_door* repo consists of three main scripts which are described in the following.
You are able to integrate these scripts in home automatization tools like OpenHAB, for 
which I will give a short introduction at the end of this readme.

## Technical requirements
* Raspberry Pi
* Raspbian
* Python 3.9

The scripts can also run under other configurations, but were only tested in the above environment.

## Config

## Coop Door
The *coop_door.py* is the main script of this repo. It is responsible for opening, closing and stopping 
the coop door. If you only want to automatically control your coop door, use this script!
The script is controlled via Mqtt and is therefore losely coupled.

|MQTT Topic| Possible Values | Description                                                                                                              |
|----------|----------------|--------------------------------------------------------------------------------------------------------------------------|
|garden/chickens/coopdoor|OPEN, CLOSE, STOP| The *coop_door.py* script is subscribed to this topic and reacts to the given value to open, stop or close the coop door |
|garden/chickens/coopdoor/state|*| Whenever a message was published to this topic, the *coop_door.py* script resets its control GPIO pins                   |


## Coop Door Buttons
This script is optional!

Additionally to the automatic coop door control, I installed buttons next to my coop door to control it manually. E.g. whenever I clean the coop
I want to do this not being disturbed by the chickens, so I close the door via buttons.

The *coop_door_buttons.py* is used as some kind of proxy. It takes the button presses and publishes commands to the mqtt topic. As we learned in the *Coop Door* section, 
the *coop_door.py* script will then listen to the topic and open, stop or close the coop door.

|MQTT Topic| Possible Values | Description                                                                           |
|----------|----------------|---------------------------------------------------------------------------------------|
|garden/chickens/coopdoor|OPEN, CLOSE, STOP| The *coop_door_buttons.py* script publishes a message depending on the button pressed |

There's one specialty for the *coop_door_buttons.py* script: Because of problems I had that the script got "ghost button pressed" events, the door sometimes opened at night or in the early morning.
Therefore, I introduced a check that the door cannot be opened or closed between 7:30 and 22:00 o'clock.
In case you don't want this check, you currently must adapt the code at line 48 and replace
```
if earliest_open_datetime < current_date_and_time < latest_open_datetime:
```
by
```
if True:
```
Perhaps this will be removed in the future or being made configurable. Let me know if this is a use case for you.


## Coop Door Sensors
This script is optional!

To see my coop doors state and ensure, the door is closed, when I expected it being closed and open, when I expect it, I installed reed sensors to my coop door.
The sensors are installed at the lowest (closed) and highest (open) point of the coop door frame. A magnet is installed on the coop door.
The sensors are connected to the Raspberry Pi.

In my configuration the sensors are the single source of truth. Means, only if a sensor publishes the coop door was opened or closed, I really trust the state.

|MQTT Topic| Possible Values         | Description                                                                                                                                                                                    |
|----------|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|garden/chickens/coopdoor/state| OPEN, CLOSED            | The *coop_door_sensors.py* script publishes a message whenever one of the coop door sensors were activated                                                                                     |
|garden/chickens/coopdoor/realtime-state| OPENED, RUNNING, CLOSED | The realtime state represents the real state of the coop door. When the sensors were activated it published OPEN or CLOSED; when both sensors were released, it publishes RUNNING |

## Installation
There are multiple ways of running the script(s). I installed all the Python libraries in a Python virtual environment.
In this example, the right Python version is already installed on the Raspberry Pi and the coop door scripts are checked out to 
```
/home/pi/coop_door
```
To install the virtual environment call the following command from your coop door script folder.

```
python -m venv coop_door
```
To activate the virtual environment run 
```
source coop_door/bin/activate
```
and run
```
pip install --upgrade pip
```
to update pip.

Next install the dependencies for the coop door scripts
```
pip install -r requirements.txt
```
Now you can run the scripts with from the shell
```
python coop_door(_sensors|_buttons).py
```
For a productive use it of course make sense to run the scripts as separate services.

You can now use a client like Mqtt.fx to send messages to your script and check the logs what's happening.

Have fun!