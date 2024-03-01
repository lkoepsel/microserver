from machine import Pin
from wlan import connect
import sys
from microdot import Microdot, send_file
from microdot.websocket import with_websocket


if not (connect()):
    print("wireless connection failed")
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
        await ws.send(data)

app.run(debug=True)
