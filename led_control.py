#!/usr/bin/env python3
import serial
import time
import argparse
from enum import Enum

class Mode(Enum):
    RAINBOW = 0x01
    BREATHING = 0x02
    COLOR_CYCLE = 0x03
    OFF = 0x04
    AUTO = 0x05

class Brightness(Enum):
    LEVEL_1 = 0x05
    LEVEL_2 = 0x04
    LEVEL_3 = 0x03
    LEVEL_4 = 0x02
    LEVEL_5 = 0x01

class Speed(Enum):
    SLOWEST = 0x05
    SLOW = 0x04
    MEDIUM = 0x03
    FAST = 0x02
    FASTEST = 0x01

PRESETS = {
    "off": (Mode.OFF, Brightness.LEVEL_5, Speed.MEDIUM),
    "rainbow": (Mode.RAINBOW, Brightness.LEVEL_5, Speed.FASTEST),
    "breathing": (Mode.BREATHING, Brightness.LEVEL_3, Speed.SLOW),
    "auto": (Mode.AUTO, Brightness.LEVEL_5, Speed.FAST),
    "cycle": (Mode.COLOR_CYCLE, Brightness.LEVEL_4, Speed.MEDIUM)
}

def calculate_checksum(a, b, c):
    return (0xFA + a + b + c) & 0xFF

def send_command(port, mode, brightness, speed):
    try:
        ser = serial.Serial(port, 10000, timeout=1)
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return False

    cmd = [
        0xFA,
        mode.value,
        brightness.value,
        speed.value,
        calculate_checksum(mode.value, brightness.value, speed.value)
    ]

    for byte in cmd:
        ser.write(bytes([byte]))
        time.sleep(0.005)

    ser.close()
    print(f"Command sent to {port}: {[hex(x) for x in cmd]}")
    return True

def list_presets():
    print("Available presets:")
    for name, (mode, brightness, speed) in PRESETS.items():
        print(f"{name:10} - Mode: {mode.name:12} Brightness: {6 - brightness.value} Speed: {6 - speed.value}")

def main():
    parser = argparse.ArgumentParser(description='LED Controller')
    parser.add_argument('-p', '--port', required=True, help='Serial port (e.g. /dev/ttyUSB0 or COM3)')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--preset', help='Use preset configuration', choices=PRESETS.keys())
    group.add_argument('--custom', action='store_true', help='Use custom settings')

    parser.add_argument('--list', action='store_true', help='List available presets')

    # Custom mode arguments
    parser.add_argument('--mode', type=int, help='Mode: 1=RAINBOW, 2=BREATHING, 3=COLOR_CYCLE, 4=OFF, 5=AUTO')
    parser.add_argument('--brightness', type=int, choices=range(1,6), help='Brightness level (1-5)')
    parser.add_argument('--speed', type=int, choices=range(1,6), help='Speed level (1-5)')

    args = parser.parse_args()

    if args.list:
        list_presets()
        return

    if args.preset:
        mode, brightness, speed = PRESETS[args.preset]
    elif args.custom:
        if not all([args.mode, args.brightness, args.speed]):
            print("Error: --custom requires --mode, --brightness and --speed")
            return

        try:
            mode = Mode(args.mode)
            brightness = Brightness(6 - args.brightness)
            speed = Speed(6 - args.speed)
        except ValueError:
            print("Invalid parameter values!")
            return

    send_command(args.port, mode, brightness, speed)

if __name__ == "__main__":
    main()
