# light_leds_v1 - browser-based method of controlling builtin LED
from machine import Pin
from microdot import Microdot, send_file
import sys


def web_server():
    # Required for WLAN on Pico W, 'machine' indicates Pico-based micropython
    # Will not differeniate between Pico and Pico W!
    if hasattr(sys.implementation, '_machine'):
        from wlan import connect
        if not (connect()):
            print(f"wireless connection failed")
            sys.exit()

    builtin = Pin("LED", Pin.OUT)

    app = Microdot()

    @app.route('/')
    def index(request):
        return send_file('templates/index.html')

    @app.post('/')
    def index_post(request):
        level = int(request.form['level'])
        builtin.value(level)
        return send_file('templates/index.html')

    @app.get('computer.svg')
    def computer_svg(request):
        return send_file('./computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
