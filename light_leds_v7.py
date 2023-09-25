# light_leds_v7 - webserver to control four leds
# refactored to simplify the program, using tuple of LEDS instead of variables
from machine import Pin
from microdot import Microdot, Response, send_file, Request
from microdot_utemplate import render_template
import sys
from pins import PicoW_pins


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
    # Required for WLAN on Pico W, 'machine' indicates Pico-based micropython
    # Will not differeniate between Pico and Pico W!
    if hasattr(sys.implementation, '_machine'):
        from wlan import connect
        if not (connect()):
            print(f"wireless connection failed")
            sys.exit()

    app = Microdot()
    Response.default_content_type = 'text/html'
    Request.socket_read_timeout = None

    @ app.route('mvp.css')
    def mvp(request):
        return send_file('templates/mvp.css', max_age=31536000)

    @ app.post('/control.html')
    def control(request):
        global leds
        if len(request.form.getlist('label')) == 4:
            set_leds(request.form)
        else:
            control_led(request.form.getlist('led'))
        return render_template('control.html', leds)

    @ app.get('/')
    def index(request):
        return send_file('templates/index.html')

    @ app.get('computer.svg')
    def computer_svg(request):
        return send_file('./computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @ app.get('favicon.png')
    def favicon(request):
        return send_file('./favicon.png', content_type='image/png')

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
