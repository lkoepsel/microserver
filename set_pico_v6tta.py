import time
from websocket import create_connection

ws = create_connection("ws://10.0.1.6:5000/ws")
interval = .01

for i in range(5):
    ws.send('true')
    time.sleep(interval)

    ws.send('false')
    time.sleep(interval)

elapsed = ws.recv()
print(f"Elapsed time: {elapsed} us")
