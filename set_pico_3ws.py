import time
from websocket import create_connection

ws = create_connection("ws://10.0.1.6:5000/ws")
response_time = .01

check = True
while True:
    ws.send(str(check))
    # ws.send(str(check).lower())

    time.sleep(response_time)
    check = not check
