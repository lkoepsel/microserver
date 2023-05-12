import time
import network
from machine import Pin, Timer
import secrets
import ubinascii


wireless = Pin("LED", Pin.OUT)


def tick(timer):
    global wireless
    wireless.toggle()


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.ssid, secrets.password)
    # toggle power mode to increase responsiveness
    wlan.config(pm=0xa11140)

    blink = Timer()

    max_wait = 10
    blink.init(freq=4, mode=Timer.PERIODIC, callback=tick)
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        blink.init(freq=20, mode=Timer.PERIODIC, callback=tick)

    else:
        blink.deinit()
        status = wlan.ifconfig()
        MAC = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
        print(f"Name: Pico W X")
        print(f"IP Address: {status[0]}")
        print(f"MAC Address: {MAC}")
        print(f"Channel: {wlan.config('channel')}")
        print(f"SSID: {wlan.config('essid')}")
        print(f"TX Power: {wlan.config('txpower')}")