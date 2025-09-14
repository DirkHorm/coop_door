#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from gpiozero import Button, OutputDevice

# Pins für Motor (Türbewegung)
MOTOR_OPEN_PIN = 16
MOTOR_CLOSE_PIN = 20

# Pins für Reed-Sensoren
SENSOR_OPEN_PIN = 19
SENSOR_CLOSE_PIN = 26

COOP_DOOR_DOWN_TIME = 5
COOP_DOOR_UP_TIME = 8

# Test-Bouncezeiten in Sekunden
BOUNCE_TIMES = [0.005, 0.01, 0.02, 0.05, 0.1]

# Motorsteuerung
motor_open = OutputDevice(MOTOR_OPEN_PIN, active_high=True, initial_value=False)
motor_close = OutputDevice(MOTOR_CLOSE_PIN, active_high=True, initial_value=False)

# Counter
event_counts = {}

def run_test(bounce_time):
    print(f"\n[=== Starting test with bounce_time={bounce_time:.3f}s ===]")

    counts = {"open_pressed": 0, "open_released": 0, "close_pressed": 0, "close_released": 0}

    open_sensor = Button(SENSOR_OPEN_PIN, pull_up=True, bounce_time=bounce_time)
    close_sensor = Button(SENSOR_CLOSE_PIN, pull_up=True, bounce_time=bounce_time)

    open_sensor.when_pressed = lambda: handle_event("OPEN_SENSOR PRESSED", bounce_time, counts, "open_pressed")
    open_sensor.when_released = lambda: handle_event("OPEN_SENSOR RELEASED", bounce_time, counts, "open_released")
    close_sensor.when_pressed = lambda: handle_event("CLOSE_SENSOR PRESSED", bounce_time, counts, "close_pressed")
    close_sensor.when_released = lambda: handle_event("CLOSE_SENSOR RELEASED", bounce_time, counts, "close_released")

    # Down
    print(">>> Coop Door DOWN")
    motor_close.on()
    time.sleep(COOP_DOOR_DOWN_TIME)
    motor_close.off()

    # Up
    print(">>> Coop Door UP")
    motor_open.on()
    time.sleep(COOP_DOOR_UP_TIME)
    motor_open.off()

    time.sleep(1)  # kurze Pause

    event_counts[bounce_time] = counts
    print(f"[=== Test with bounce_time={bounce_time:.3f}s finished ===]\n")

def handle_event(msg, bt, counts, key):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] [{msg}] (bt={bt:.3f})")
    counts[key] += 1

def main():
    for bt in BOUNCE_TIMES:
        run_test(bt)

    print("\n=== Statistik über alle Tests ===")
    for bt, counts in event_counts.items():
        print(f"bounce_time={bt:.3f}s → OPEN pressed={counts['open_pressed']}, "
              f"OPEN released={counts['open_released']}, "
              f"CLOSE pressed={counts['close_pressed']}, "
              f"CLOSE released={counts['close_released']}")

    print("\nAlle Tests abgeschlossen! Bitte Ergebnisse vergleichen.")

if __name__ == "__main__":
    main()
