import time
from websocket import create_connection
import json

ws = create_connection("ws://10.0.1.6:5000/ws")
interval = .01
max_sessions = 20

for i in range(max_sessions):
    ws.send('true')
    time.sleep(interval)

    ws.send('false')
    time.sleep(interval)

raw = ws.recv()
n_times = json.loads(raw)
for n in n_times:
    print(f"Elapsed time: {n} ms")
