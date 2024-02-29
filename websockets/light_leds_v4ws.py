import json
from machine import Pin
from wlan import connect
import sys
from microdot import Microdot, send_file
from microdot.websocket import with_websocket


def web_server():
    if not (connect()):
        print("wireless connection failed")
        sys.exit()

    yellow = Pin(2, Pin.OUT)
    green = Pin(15, Pin.OUT)
    red = Pin(16, Pin.OUT)
    blue = Pin(22, Pin.OUT)

    leds = [yellow, green, red, blue]
    app = Microdot()

    @app.route('/')
    async def index(request):
        return send_file('templates/index.html')

    @app.get('computer.svg')
    def computer_svg(request):
        return send_file('./computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('on_green.svg')
    def on_green_svg(request):
        return send_file('./on_green.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('on_yellow.svg')
    def on_yellow_svg(request):
        return send_file('./on_yellow.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('on_red.svg')
    def on_red_svg(request):
        return send_file('./on_red.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('on_blue.svg')
    def on_blue_svg(request):
        return send_file('./on_blue.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('off.svg')
    def off_svg(request):
        return send_file('./off.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @ app.route('mvp.css')
    async def mvp(request):
        return send_file('templates/mvp.css', max_age=31536000)

    @ app.route('style_v4ws.css')
    async def style_v4ws(request):
        return send_file('templates/style_v4ws.css', max_age=31536000)

    @ app.get('favicon.ico')
    async def favicon_ico(request):
        return send_file('./favicon.ico', max_age=31536000)

    @app.route('/ws')
    @with_websocket
    async def ws(request, ws):
        while True:
            raw = await ws.receive()
            print(f"{raw=}")
            data = json.loads(raw)
            leds[data['i']].value(int(data['checkbox']))

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
