from wlan import connect
import sys
from microdot import Microdot, send_file
from microdot.websocket import with_websocket
from time import ticks_us, ticks_diff


def web_server():
    if not (connect()):
        print("wireless connection failed")
        sys.exit()

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

    @ app.route('style_v5tt.css')
    async def style_v5tt(request):
        return send_file('templates/styles/style_v5tt.css', max_age=31536000)

    @ app.get('favicon.ico')
    async def favicon_ico(request):
        return send_file('../favicon.ico', max_age=31536000)

    @app.route('/ws')
    @with_websocket
    async def ws(request, ws):
        while True:
            data = await ws.receive()
            if data == 'true':
                start = ticks_us()
            elif data == 'false':
                elapsed = ticks_diff(ticks_us(), start)
                await ws.send(str(elapsed))
            else:
                print(f"{data} sent, value must be boolean")

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
