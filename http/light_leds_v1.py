# light_leds_v1 - browser-based method of controlling builtin LED
from machine import Pin
from microdot import Microdot, send_file
import sys
from wlan import connect


def web_server():
    if not (connect()):
        print("wireless connection failed")
        sys.exit()

    builtin = Pin("LED", Pin.OUT)

    app = Microdot()

    @app.route('/')
    def index(request):
        return send_file('../templates/index.html')

    @app.post('/')
    def index_post(request):
        level = int(request.form['level'])
        builtin.value(level)
        return send_file('../templates/index.html')

    @app.get('computer.svg')
    def computer_svg(request):
        return send_file('../images/computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
