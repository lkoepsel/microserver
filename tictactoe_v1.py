# tictactoe_v1 - simple tic-tac-toe game using micropython, microdot server
from microdot import Microdot, Response, send_file, Request
from microdot_utemplate import render_template
import time
import network
from machine import Pin, Timer
import secrets


wireless = Pin("LED", Pin.OUT)
yellow = Pin(2, Pin.OUT)
green = Pin(15, Pin.OUT)
white = Pin(16, Pin.OUT)
blue = Pin(22, Pin.OUT)


def tick(timer):
    global wireless
    wireless.toggle()


def set_led(color, level):
    if color == 'WHITE':
        white.value(int(level))
    if color == 'GREEN':
        green.value(int(level))
    if color == 'BLUE':
        blue.value(int(level))
    if color == 'YELLOW':
        yellow.value(int(level))


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.ssid, secrets.password)

blink = Timer()

max_wait = 10
blink.init(freq=4, mode=Timer.PERIODIC, callback=tick)
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    time.sleep(1)


# Handle connection error
if wlan.status() != 3:
    blink.init(freq=20, mode=Timer.PERIODIC, callback=tick)

else:
    blink.deinit()
    status = wlan.ifconfig()
    print('ip = ' + status[0])


app = Microdot()
Response.default_content_type = 'text/html'
Request.socket_read_timeout = None


marks = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
disabled = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
pico_plays = [[0, 1], [2, 0], [2, 2],
              [1, 1], [0, 2], [1, 0],
              [1, 2], [0, 0], [2, 1]]
pico = 0


def init():
    global pico
    for i in range(3):
        for j in range(3):
            marks[i][j] = ' '
            disabled[i][j] = ' '
    pico = 0
    # print(f"INIT{pico=}{marks=}{disabled=}")
    return marks, disabled


def pico_play(t):
    while(t):
        global pico

        if marks[pico_plays[pico][0]][pico_plays[pico][1]] == 'X':
            if pico >= 8:
                # print(f"Pentultimate spot!{pico=}")
                return True
            pico += 1

        else:
            t = False
            set_mark(pico_plays[pico][0], pico_plays[pico][1], 'O')
            pico += 1

    return


def check_path(p):
    if marks[0][0] == p and marks[0][1] == p and marks[0][2] == p:
        return True
    elif marks[1][0] == p and marks[1][1] == p and marks[1][2] == p:
        return True
    elif marks[2][0] == p and marks[2][1] == p and marks[2][2] == p:
        return True
    elif marks[0][0] == p and marks[1][1] == p and marks[2][2] == p:
        return True
    elif marks[0][2] == p and marks[1][1] == p and marks[2][0] == p:
        return True
    elif marks[0][2] == p and marks[1][2] == p and marks[2][2] == p:
        return True
    elif marks[0][1] == p and marks[1][1] == p and marks[2][1] == p:
        return True
    elif marks[0][0] == p and marks[1][0] == p and marks[2][0] == p:
        return True
    else:
        return False


def set_mark(r, c, p):
    marks[r][c] = p
    disabled[r][c] = 'disabled'
    return marks, disabled


@app.route('/', methods=['GET', 'POST'])
def index(request):
    global pico
    turn = True
    square = None
    if request.method == 'POST':
        if 'square' in request.form.keys():
            square = request.form['square']
            row = int(square[:1])
            col = int(square[1:2])

            markup = set_mark(row, col, 'X')
            draw = pico_play(turn)
            if draw:
                return send_file('./draw.html')
            lost = check_path('O')
            won = check_path('X')
            if lost:
                return send_file('./lost.html')
            elif won:
                return send_file('./won.html')
            else:
                return render_template('index.html',
                                       marks=markup[0], disabled=markup[1])
        elif 'play' in request.form.keys():
            init()
            if request.form['play'] == 'Play Again?':
                return render_template('index.html', marks=marks,
                                       disabled=disabled)
    else:
        # print(pico_plays)
        return render_template('index.html', marks=marks, disabled=disabled)


@app.post('/won.html')
def won_post(request):
    return render_template('index.html', marks=marks, disabled=disabled)


@app.post('/lost.html')
def lost_post(request):
    return render_template('index.html', marks=marks, disabled=disabled)


@app.post('/draw.html')
def draw_post(request):
    return render_template('index.html', marks=marks, disabled=disabled)


@app.route('bulma.min.css')
def bulma(request):
    return send_file('./bulma.min.css', max_age=31536000)


@app.get('favicon.png')
def favicon(request):
    return send_file('./favicon.png', content_type='image/png')


@app.get('computer.svg')
def computer_svg(request):
    return send_file('./computer.svg', content_type='image/svg+xml',
                     max_age=31536000)


app.run(debug=True)
