# light_leds - browser-based method of controlling leds
from machine import Pin
from microdot import Microdot, Response, send_file, Request
from microdot_utemplate import render_template
import sys


yellow = Pin(2, Pin.OUT)
green = Pin(15, Pin.OUT)
red = Pin(16, Pin.OUT)
blue = Pin(22, Pin.OUT)
led_state = ['', '', '', '']
leds = [['yellow', 4], ['green', 20], ['red', 21], ['blue', 29]]
confirmed = False


def set_led(leds):
    global led_state
    print(f"{leds}")
    if len(leds) == 0:
        yellow.value(0)
        green.value(0)
        red.value(0)
        blue.value(0)
        led_state = ['' for _ in range(4)]
    else:
        for led in leds:
            if 'YELLOW' in leds:
                yellow.value(1)
                led_state[0] = 'checked'
            else:
                yellow.value(0)
                led_state[0] = ''
            if 'GREEN' in leds:
                green.value(1)
                led_state[1] = 'checked'
            else:
                green.value(0)
                led_state[1] = ''
            if 'RED' in leds:
                red.value(1)
                led_state[2] = 'checked'
            else:
                red.value(0)
                led_state[2] = ''
            if 'BLUE' in leds:
                blue.value(1)
                led_state[3] = 'checked'
            else:
                blue.value(0)
                led_state[3] = ''


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


@app.route('marx.css')
def marx(request):
    return send_file('templates/marx.css', max_age=31536000)


@app.route('/', methods=['GET', 'POST'])
def index(request):
    global led_state
    if request.method == 'POST':
        set_led(request.form.getlist('led'))
        return render_template('index.html', led_state, leds, confirmed)
    else:
        return render_template('index.html', led_state, leds, confirmed)


@app.get('computer.svg')
def computer_svg(request):
    return send_file('./computer.svg',
                     content_type='image/svg+xml', max_age=31536000)


@app.get('favicon.png')
def favicon(request):
    return send_file('./favicon.png', content_type='image/png')


app.run(debug=True)
