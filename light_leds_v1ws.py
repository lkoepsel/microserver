from machine import Pin
from wlan import connect
import sys
from microdot import Microdot, send_file
from microdot.websocket import with_websocket


if not (connect()):
    print(f"wireless connection failed")
    sys.exit()

builtin = Pin("LED", Pin.OUT)

app = Microdot()


@app.route('/')
async def index(request):
    return send_file('templates/index.html')


@app.route('/echo')
@with_websocket
async def echo(request, ws):
    while True:
        data = await ws.receive()
        if data == 'on':
            builtin.value(1)
        elif data == 'off':
            builtin.value(0)
        else:
            await ws.send(data)

app.run(debug=True)
