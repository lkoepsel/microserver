from math import pow
import sys
import time
from websocket import create_connection

ws = create_connection("ws://10.0.1.6:5000/ws")
interval = 10
interval_ms = interval * pow(10, -3)


def main():
    print(f"Testing with {interval_ms} s, press Ctrl+C to quit")
    while True:
        ws.send('true')
        time.sleep(interval_ms)

        ws.send('false')
        elapsed = int(ws.recv()) / 1000
        delta = ((elapsed - interval) / elapsed) * 100
        print(f"Elapsed time: {elapsed:8.2f} ms, % delta: {delta:6.2f} ")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Stopped Test')
        sys.exit(0)
