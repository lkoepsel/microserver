from machine import Pin
from wlan import connect
import sys
from microdot import Microdot, send_file
from microdot.websocket import with_websocket


def web_server():
    if not (connect()):
        print("wireless connection failed")
        sys.exit()

    builtin = Pin("LED", Pin.OUT)

    app = Microdot()

    @app.route('/')
    async def index(request):
        return send_file('templates/index.html')

    @app.get('computer.svg')
    def computer_svg(request):
        return send_file('../images/computer.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('on.svg')
    def on_svg(request):
        return send_file('../images/on.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @app.get('off.svg')
    def off_svg(request):
        return send_file('../images/off.svg',
                         content_type='image/svg+xml', max_age=31536000)

    @ app.route('mvp.css')
    async def mvp(request):
        return send_file('templates/styles/mvp.css', max_age=31536000)

    @ app.route('style_v2ws.css')
    async def style_v2ws(request):
        return send_file('templates/styles/style_v2ws.css', max_age=31536000)

    @ app.get('favicon.ico')
    async def favicon_ico(request):
        return send_file('./favicon.ico', max_age=31536000)

    @app.route('/ws')
    @with_websocket
    async def ws(request, ws):
        while True:
            # in steps to show the values being transmitted, w/ error checks
            # data = await ws.receive()

            # with error checking
            # if data == 'on':
            #     builtin.value(1)
            # elif data == 'off':
            #     builtin.value(0)
            # else:
            #     print("Error occured, value must be 'on' or 'off'")

            # or refactored, w/o error checking
            # requires radio buttons to send '1' and '0', not 'on' or 'off'
            builtin.value(int(await ws.receive()))

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
