# light_leds_v2 - browser-based method of controlling leds
from machine import Pin
from microdot import Microdot, send_file
import sys
from wlan import connect


yellow = Pin(2, Pin.OUT)
green = Pin(15, Pin.OUT)
red = Pin(16, Pin.OUT)
blue = Pin(22, Pin.OUT)


def set_led(color, level):
    if color == 'RED':
        red.value(int(level))
    if color == 'GREEN':
        green.value(int(level))
    if color == 'BLUE':
        blue.value(int(level))
    if color == 'YELLOW':
        yellow.value(int(level))


def web_server():
    if not (connect()):
        print("wireless connection failed")
        sys.exit()

    app = Microdot()

    @app.route('/')
    def index(request):
        return send_file('templates/index.html')

    @app.post('/')
    def index_post(request):
        level = request.form['level']
        led = request.form['led']
        print("Set", led, "led", level)
        set_led(led, level)
        return send_file('templates/index.html')

    @app.get('computer.svg')
    def computer_svg(request):
        return send_file('../images/computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
