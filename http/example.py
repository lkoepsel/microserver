# example - simple program to demo Pico W-based web server
# 1. setup wireless lan
# 2. set up the webserver
# 3. allow the program to be called from the REPL
# Required for success on the board:
# microdot.py, wlan.py, example.py, secrets.py (manual copy)
from microdot import Microdot
import sys


# 1. this code sets up the wlan
def web_server():
    # Required for WLAN on Pico W, 'machine' indicates Pico-based micropython
    # Will not differentiate between Pico and Pico W!
    if hasattr(sys.implementation, '_machine'):
        from wlan import connect
        if not (connect()):
            print(f"wireless connection failed")
            sys.exit()

    # 2. this code sets up the webserver
    app = Microdot()

    @app.route('/')
    def index(request):
        return 'Hello, World!'

    app.run(port=5001, debug=True)


# 3. allows us to debug calling web_server manually (REPL)
if __name__ == '__main__':
    web_server()
