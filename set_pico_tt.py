import time
from websocket import create_connection

ws = create_connection("ws://10.0.1.6:5000/ws")
response_time = .01

while True:
    ws.send('true')
    time.sleep(response_time)

    ws.send('false')
    time.sleep(response_time)
    elapsed = ws.recv()
    print(f"Elapsed time: {elapsed} us")
