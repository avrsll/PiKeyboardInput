import socket
import pyautogui
import json

def parse_event(event_json):
    return json.loads(event_json)

# Set up network connection to the Raspberry Pi
HOST = 'raspberrypi.local'  # The hostname or IP address of your Raspberry Pi
PORT = 50007  # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

try:
    while True:

        # Receive JSON event from Raspberry Pi
        data = s.recv(1024)
        if not data:
            break

        # Parse the event data from JSON
        event = parse_event(data.decode('utf-8'))

        # Now, handle the parsed event data:
        if event['type'] == 'key':
            pyautogui.press(event.key)
        elif event['type'] == 'mouse':
            pyautogui.move(event.dx, event.dy)
        elif event.type == 'click':
            pyautogui.click()
finally:
    s.close()