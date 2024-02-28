from wlan import connect
import sys
from microdot import Microdot, send_file
from microdot.websocket import with_websocket
from time import ticks_us, ticks_diff


# Pseudo-code for the Pi Pico side
elapsed_times = []
session_count = 0
max_sessions = 20  # Number of sessions before sending data back


async def save_times(t, ws):
    global session_count
    elapsed_times.append(t)
    session_count += 1
    if session_count >= max_sessions:
        await ws.send(str(elapsed_times))
        print(f"{elapsed_times}")
        elapsed_times.clear()
        session_count = 0


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

    @ app.route('style_v5tt.css')
    async def style_v5tt(request):
        return send_file('templates/style_v5tt.css', max_age=31536000)

    @ app.get('favicon.ico')
    async def favicon_ico(request):
        return send_file('./favicon.png', max_age=31536000)

    @app.route('/ws')
    @with_websocket
    async def ws(request, ws):
        global session_count
        while True:
            data = await ws.receive()
            if data == 'true':
                start = ticks_us()
            elif data == 'false':
                elapsed = ticks_diff(ticks_us(), start)
                await save_times(elapsed, ws)

            else:
                print(f"{data} sent, value must be boolean")

    app.run(debug=True)


if __name__ == '__main__':
    web_server()
