import json
import time
from websocket import create_connection

ws = create_connection("ws://10.0.1.6:5000/ws")
response_time = .04

check = True
while True:
    for i in range(4):
        ws.send(json.dumps({"i": i, "checkbox": check}))

    time.sleep(response_time)
    check = not check
