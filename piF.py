import json
import socket
from evdev import InputDevice, categorize, ecodes

# Set up the device path for keyboard and mouse
keyboard = InputDevice('/dev/input/event3')  # Replace with your keyboard device
mouse = InputDevice('/dev/input/event1')     # Replace with your mouse device

# Set up the network connection
HOST = ''                                   # Symbolic name meaning all available interfaces
PORT = 50007                                # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

print('Connected by', addr)

try:
    while True:
        # Handle keyboard events
        keyboard_event = keyboard.read_one()
        if keyboard_event:
            # Convert keyboard event to JSON
            key_event_json = json.dumps({
                'type': 'key',
                'code': keyboard_event.code,
                'value': keyboard_event.value
            })
            conn.sendall(key_event_json.encode())

        # Handle mouse events
        mouse_event = mouse.read_one()
        if mouse_event:
            # Convert mouse event to JSON
            mouse_event_json = json.dumps({
                'type': 'mouse',
                'code': mouse_event.code,
                'value': mouse_event.value
            })
            conn.sendall(mouse_event_json.encode())
finally:
    conn.close()
    s.close()