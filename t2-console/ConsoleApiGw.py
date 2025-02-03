import traceback

from flask import Flask, request, Response, render_template, send_from_directory
from flask_cors import CORS
import json
from werkzeug.exceptions import HTTPException

import data_models

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CONSOLE_IP = '0.0.0.0'
CONSOLE_IP_PORT = 11000

@app.route('/api/console-t2/home', methods=['GET', 'POST'])
def home():
   return send_from_directory('static','index.html'), 200

@app.route('/api/console-t2/index.css', methods=['GET', 'POST'])
def home_css():
   return send_from_directory('static','index.css'), 200



@app.route("/api/console-t2/get_algorithm_list", methods=['GET'])
def get_algorithm_list():
    return json.dumps(data_models.algorithm_list), 200


if __name__ == '__main__':
    # app.run(ssl_context=("cert.pem","key.pem"),host=MEC_IP, port=MEC_IP_PORT) # https
    app.run(host=CONSOLE_IP, port=CONSOLE_IP_PORT)