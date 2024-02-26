# from machine import Pin
from wlan import connect
import sys
from time import ticks_us, ticks_diff
from microdot import Microdot, send_file
from microdot.websocket import with_websocket


def web_server():
    if not (connect()):
        print("wireless connection failed")
        sys.exit()

    # only one blink_led can be defined, based on built-in or external led
    # blink_led = Pin("LED", Pin.OUT)
    # blink_led = Pin(16, Pin.OUT)

    app = Microdot()

    @app.route('/')
    async def index(request):
        return send_file('templates/index.html')

    @app.get('computer.svg')
    def computer_svg(request):
        return send_file('./computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('on.svg')
    def on_svg(request):
        return send_file('./on.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('off.svg')
    def off_svg(request):
        return send_file('./off.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @ app.route('mvp.css')
    async def mvp(request):
        return send_file('templates/mvp.css', max_age=31536000)

    @ app.route('style_v3ws.css')
    async def style_v3ws(request):
        return send_file('templates/style_v3ws.css', max_age=31536000)

    @ app.get('favicon.ico')
    async def favicon_ico(request):
        return send_file('./favicon.png', max_age=31536000)

    @app.route('/ws')
    @with_websocket
    async def ws(request, ws):
        while True:
            data = await ws.receive()
            print(f"{data=}")
            if data == 'true':
                start = ticks_us()
            elif data == 'false':
                elasped = ticks_diff(ticks_us(), start)
                print(f"{elasped}")
            else:
                print(f"{data} sent, value must be true/false")

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
