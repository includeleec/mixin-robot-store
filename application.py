from flask import Flask
from ws_app import wsThread


app = Flask(__name__)

@app.route("/")
def hello():

    ws = wsThread()
    ws.start()
    return "Mixin Robot Store"