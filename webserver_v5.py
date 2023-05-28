# light_leds - browser-based method of controlling leds
from machine import Pin
from microdot import Microdot, Response, send_file, Request
from microdot_utemplate import render_template
import sys
from typing import NamedTuple


# dictionary leds:
#    key: color [pin, gpio, state]
leds = {}

# PicoW Pin Numbering
PicoW_pins = [[0, 'Not a pin'],     # 0 Index, not a valid pin
              [0, 'UART0 TX'],      # Pin 1
              [0, 'UART0 RX'],
              [0, 'GND'],
              [2, 'GP2'],
              [3, 'GP3'],
              [4, 'GP4'],
              [5, 'GP5'],
              [0, 'GND'],
              [6, 'GP6'],
              [7, 'GP7'],         # Pin 10
              [8, 'GP8'],
              [9, 'GP9'],
              [0, 'GND'],
              [10, 'GP10'],
              [11, 'GP11'],
              [12, 'GP12'],
              [13, 'GP13'],
              [0, 'GND'],
              [14, 'GP14'],
              [15, 'GP15'],         # Pin 20
              [16, 'GP16'],
              [17, 'GP17'],
              [0, 'GND'],
              [18, 'GP18'],
              [19, 'GP19'],
              [20, 'GP20'],
              [21, 'GP21'],
              [0, 'GND'],
              [22, 'GP22'],
              [0, 'RUN'],         # Pin 30
              [0, 'ADC0'],
              [0, 'ADC1'],
              [0, 'AGND'],
              [0, 'ADC2'],
              [0, 'ADC_REF'],
              [0, '3V3(OUT)'],
              [0, '3V3_EN'],
              [0, 'GND'],
              [0, 'VSYS'],
              [0, 'VBUS']         # Pin 40
              ]


def set_leds(r):
    global leds
    print(f"set_leds_start{leds}")
    leds[0].color = r.get('color_0')
    leds[0].pin = PicoW_pins[r.get('pin_0')][0]
    leds[0].led = Pin(leds[0].pin, Pin.OUT)
    leds[0].state = ''
    leds[1].color = r.get('color_1')
    leds[1].pin = PicoW_pins[r.get('pin_1')][0]
    leds[1].led = Pin(leds[0].pin, Pin.OUT)
    leds[1].state = ''
    leds[2].color = r.get('color_2')
    leds[2].pin = PicoW_pins[r.get('pin_2')][0]
    leds[2].led = Pin(leds[0].pin, Pin.OUT)
    leds[2].state = ''
    leds[3].color = r.get('color_3')
    leds[3].pin = PicoW_pins[r.get('pin_3')][0]
    leds[3].led = Pin(leds[0].pin, Pin.OUT)
    leds[3].state = ''
    print(f"set_leds_end{leds}")


def control_led(c_leds):
    global leds
    print(f"control_leds_start{leds}")
    if len(leds) == 0:
        for i in range(4):
            leds[i].led.value(0)
            leds[i].state = ''
    else:
        for c_led in c_leds:
            for i in range(4):
                if leds[i].color in leds:
                    leds[i].value(1)
                    leds[i].state = 'checked'
                else:
                    leds[i].value(0)
                    leds[i].state = ''
    print(f"control_leds_end{leds}")


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


@app.post('/control.html')
def control(request):
    global led_state, leds
    if 'led' in request.form.keys():
        control_led(request.form.getlist('led'))
    else:
        print(f"control_else{leds}")
        set_leds(request.form)
    return render_template('control.html', leds)


@app.get('/')
def index(request):
    return send_file('templates/index.html')


@app.get('computer.svg')
def computer_svg(request):
    return send_file('./computer.svg',
                     content_type='image/svg+xml', max_age=31536000)


@app.get('favicon.png')
def favicon(request):
    return send_file('./favicon.png', content_type='image/png')


app.run(debug=True)
