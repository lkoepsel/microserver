# light_leds_v7 - webserver to control four leds
# refactored to simplify the program, using tuple of LEDS instead of variables
from machine import Pin
from microdot import Microdot, Response, send_file, Request
from microdot.utemplate import Template
import sys
from pins import PicoW_pins
from wlan import connect


# class LED contains the attributes for each led
# label - text for naming the led
# pin - Pico pin number (1-40)
# gpio - RP2040 GPIO number (see pins.py for xreference)
# state - on (checked) or off (blank)
# set_leds will assign values based on initial index.html form
# control_leds will update 'state' based on control.html form
class Led(object):
    def __init__(self, label, pin, gpio, state):
        self.label = label
        self.pin = pin
        self.gpio = gpio
        self.state = state

    def __repr__(self):
        return f'{self.__class__.__name__}\
        ("{self.label}", {self.pin}, {self.gpio}, "{self.state}")'


led_0 = Led
led_1 = Led
led_2 = Led
led_3 = Led
leds = [led_0, led_1, led_2, led_3]

# default pin values on webpage
def_pins = [['pin1', 4, 'Yellow'], ['pin2', 20, 'Green'],
            ['pin2', 21, 'Red'], ['pin3', 29, 'Blue']]


# function called from index.html to setup the labels and GPIO pins for leds
# request "r" has two lists, 'label' and 'pin'
def set_leds(r):
    global leds

    labels = r.getlist('label')
    pins = r.getlist('pin')

    for i, label in enumerate(labels):
        leds[i] = Led(label,
                      int(pins[i]),
                      PicoW_pins[int(pins[i])][0],
                      '')
        Pin(leds[i].gpio, Pin.OUT, value=0)


# function called from control.html to turn leds on/off
# if entry with empty list, all leds will be turned off
# else entry with list containing assigned labels will be turned on
def control_led(r_leds):
    global leds
    if len(r_leds) == 0:
        for led in leds:
            Pin(led.gpio, Pin.OUT, value=0)
            led.state = ''
    else:
        for led in leds:
            if led.label in r_leds:
                Pin(led.gpio, Pin.OUT, value=1)
                led.state = 'checked'
            else:
                Pin(led.gpio, Pin.OUT, value=0)
                led.state = ''


def web_server():
    if not (connect()):
        print("wireless connection failed")
        sys.exit()

    app = Microdot()
    Response.default_content_type = 'text/html'
    Request.socket_read_timeout = None

    @ app.route('mvp.css')
    async def mvp(request):
        return send_file('templates/styles/mvp.css', max_age=31536000)

    @ app.post('/control.html')
    async def control(request):
        global leds
        # if len(labels list) > 0, its first time through
        # set labels and pin assignments
        if len(request.form.getlist('label')) > 0:
            set_leds(request.form)

        # else, just turn the leds on/off
        else:
            control_led(request.form.getlist('led'))
        return Template('control.html').render(leds)

    @ app.get('/')
    async def index(request):
        return Template('index.html').render(def_pins)

    @ app.get('computer.svg')
    async def computer_svg(request):
        return send_file('../images/computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @ app.get('favicon.ico')
    async def favicon_ico(request):
        return send_file('./favicon.ico', max_age=31536000)

    app.run(port=5000, debug=True)


if __name__ == '__main__':
    web_server()
