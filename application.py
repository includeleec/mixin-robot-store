from flask import Flask
from lib.mixin_ws_api import MIXIN_WS_API
import ws_app


app = Flask(__name__)

@app.route("/")
def hello():
    mixin_ws = MIXIN_WS_API(on_message=ws_app.on_message)
    mixin_ws.run()
    return "Hello World!"