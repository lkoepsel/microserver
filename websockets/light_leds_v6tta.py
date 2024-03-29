from wlan import connect
import sys
from microdot import Microdot, Response, send_file, Request
from microdot.utemplate import Template
from microdot.websocket import with_websocket
from time import ticks_us, ticks_diff


# Pseudo-code for the Pi Pico side
elapsed_times = []
session_count = 0
max_sessions = 10  # Number of sessions before sending data back


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
    Response.default_content_type = 'text/html'
    Request.socket_read_timeout = None

    @app.route('/', methods=['GET'])
    async def index(request):
        global max_sessions
        return Template('index.html').render(max_sessions)

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

    @ app.route('style_v6tta.css')
    async def style_v6tta(request):
        return send_file('templates/styles/style_v6tta.css', max_age=31536000)

    @ app.get('favicon.ico')
    async def favicon_ico(request):
        return send_file('./favicon.ico', max_age=31536000)

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
