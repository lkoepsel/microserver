# tictactoe_v1 - simple tic-tac-toe game using micropython, microdot server
from microdot import Microdot, Response, send_file, Request
from microdot_utemplate import render_template
from random import randint
import re
import sys


# Required for WLAN on Pico W, 'machine' indicates Pico-based micropython
# Will not differeniate between Pico and Pico W!
if hasattr(sys.implementation, '_machine'):
    from wlan import connect
    connect()


app = Microdot()
Response.default_content_type = 'text/html'
Request.socket_read_timeout = None


m = re.compile('ZZ')
radio = '<input type="radio" name="square" value="ZZ">'
markX = '<strong>X</strong>'
markO = '<strong>O</strong>'
marks = [['', '', ''],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]

pico_plays = [[0, 1], [2, 0], [2, 2],
              [1, 1], [0, 2], [1, 0],
              [1, 2], [0, 0], [2, 1]]
pico = randint(0, 9)
size = 9
plays = 0


def init():
    global pico, plays
    for i in range(3):
        for j in range(3):
            v = str(i) + str(j)
            marks[i][j] = m.sub(v, radio)
    pico = randint(0, 9)
    plays = 0
    return marks


def pico_play(t):
    while(t):
        global pico, plays, size

        if marks[pico_plays[pico][0]][pico_plays[pico][1]] == markX:
            if plays >= 8:
                return True
            plays += 1
            pico = (pico + 1) % size

        else:
            t = False
            set_mark(pico_plays[pico][0], pico_plays[pico][1], markO)
            plays += 1
            pico = (pico + 1) % size

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
    return marks


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

            set_mark(row, col, markX)
            draw = pico_play(turn)
            if draw:
                return send_file('./draw.html')
            lost = check_path(markO)
            won = check_path(markX)
            if lost:
                return send_file('./lost.html')
            elif won:
                return send_file('./won.html')
            else:
                return render_template('index.html',
                                       marks=marks)
        elif 'play' in request.form.keys():
            init()
            if request.form['play'] == 'Play Again?':
                return render_template('index.html', marks=marks)
    else:
        return render_template('index.html', marks=marks)


@app.post('/won.html')
def won_post(request):
    init()
    return render_template('index.html', marks=marks)


@app.post('/lost.html')
def lost_post(request):
    init()
    return render_template('index.html', marks=marks)


@app.post('/draw.html')
def draw_post(request):
    init()
    return render_template('index.html', marks=marks)


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


init()
app.run(debug=True)
