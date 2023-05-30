# light_leds - browser-based method of controlling leds
from machine import Pin
from microdot import Microdot, Response, send_file, Request
from microdot_utemplate import render_template
import sys


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
labels = []
pins = []
gpio = []
states = []
levels = []


def set_leds(r):
    global labels, pins, gpio, states, levels

    labels.append(r.get('color_0'))
    pins.append(int(r.get('pin_0')))
    gpio.append(PicoW_pins[int(r.get('pin_0'))][0])
    states.append('')
    levels.append(0)
    Pin(gpio[0], Pin.OUT, value=0)

    labels.append(r.get('color_1'))
    pins.append(int(r.get('pin_1')))
    gpio.append(PicoW_pins[int(r.get('pin_1'))][0])
    states.append('')
    levels.append(0)
    Pin(gpio[1], Pin.OUT, value=0)

    labels.append(r.get('color_2'))
    pins.append(int(r.get('pin_2')))
    gpio.append(PicoW_pins[int(r.get('pin_2'))][0])
    states.append('')
    levels.append(0)
    Pin(gpio[2], Pin.OUT, value=0)

    labels.append(r.get('color_3'))
    pins.append(int(r.get('pin_3')))
    gpio.append(PicoW_pins[int(r.get('pin_3'))][0])
    states.append('')
    levels.append(0)
    Pin(gpio[3], Pin.OUT, value=0)


def control_led(r_leds):
    global labels, states, gpio
    if len(r_leds) == 0:
        for i in range(4):
            Pin(gpio[i], Pin.OUT, value=0)
            states[i] = ''
    else:
        for i in range(4):
            if labels[i] in r_leds:
                Pin(gpio[i], Pin.OUT, value=1)
                states[i] = 'checked'
            else:
                Pin(gpio[i], Pin.OUT, value=0)
                states[i] = ''


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

    @ app.route('marx.css')
    def marx(request):
        return send_file('templates/marx.css', max_age=31536000)

    @ app.post('/control.html')
    def control(request):
        global leds
        if 'color_0' in request.form.keys():
            set_leds(request.form)
        else:
            control_led(request.form.getlist('led'))
        return render_template('control.html', labels, pins, states)

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
