# wlan_v2 - wireless lan connection, use LEDs for status
from microdot import Microdot, send_file


app = Microdot()


@app.route('/')
def index(request):
    return send_file('./index.html')


@app.post('/')
def index_post(request):
    square = request.form['square']
    print("Row", square[:1], "Col", square[1:2])
    return send_file('./index.html')


@app.route('bulma.min.css')
def bulma(request):
    return send_file('./bulma.min.css')


@app.get('favicon.png')
def favicon(request):
    return send_file('./favicon.png', content_type='image/png')


@app.get('computer.svg')
def computer_svg(request):
    return send_file('./computer.svg', content_type='image/svg+xml')


app.run(debug=True)
