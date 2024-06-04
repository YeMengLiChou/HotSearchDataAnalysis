from flask import Flask
from flask import request

app = Flask(__name__)





@app.get("/hot/")
def get_hot_data():
    start_time = request.args.get("start")
    app.logger.info(start_time)
