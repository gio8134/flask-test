import traceback

from flask import Flask, request, Response
from flask_cors import CORS
import json
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv

from config.module_context import MContext

# Load variables from the .env file
# load_dotenv()
load_dotenv(dotenv_path="./mock.env")

app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
MEC_IP = '0.0.0.0'
MEC_IP_PORT = 10000


def handle_request(system_to_invoke_str, method, request):
    print(f' ------- START {system_to_invoke_str} {method} ------- ', flush=True)
    try:
        print(f'Received \n'
              f'METHOD: {request.method} - PATH: {request.path} - QUERY PARAMS: {request.args.to_dict()}\n'
              f'BODY: {request.data}', flush=True)
        system_to_invoke_obj = getattr(MContext, system_to_invoke_str)
        response = getattr(system_to_invoke_obj, method)(request)
        print(f'Response {response}', flush=True)
    except Exception as e:
        print(e, flush=True)
        print(traceback.format_exc(), flush=True)
        error = {
            "error": "Unexpected error",
            "code": 500,
            "message": f'{e}'
        }
        response = Response(json.dumps(error), status=500, mimetype='application/json')
    print(f' ------- END {system_to_invoke_str} {method} ------- ', flush=True)
    return response


@app.route("/api/ses/ses_trigger", methods=['POST'])
def ses_trigger():
    return handle_request('ses', 'trigger', request=request)


@app.route("/api/ses/check_result_ses_trigger", methods=['GET'])
def check_ses_result():
    return handle_request('ses', 'check_result', request=request)


@app.route("/api/elo/elo_trigger", methods=['POST'])
def elo_trigger():
    return handle_request('elo', 'trigger', request=request)


@app.route("/api/ses/get_network_inventory", methods=['GET'])
def get_network_inventory():
    return handle_request('inventory', 'get_inventory', request=request)


@app.route("/api/ses/get_network_kpi_trend", methods=['GET'])
def get_network_kpi_trend():
    return handle_request('monitoring', 'get_kpi', request=request)


# mock paths
@app.route("/graphql/", methods=['POST'])
def mock_inventory():
    return handle_request('mock', 'get_netbox_response', request=request)


@app.route("/v3/api/ses/get_network_kpi_trend", methods=['GET'])
def mock_monitoring():
    return handle_request('mock', 'get_tim_monitoring_response', request=request)


# mock paths
@app.route("/admin/elo", methods=['GET'])
def mock_orchestrator():
    return handle_request('mock', 'get_orchestrator_response', request=request)
# mock paths
@app.route("/api/elo/v1/nef_translate_mobile_ip_to_cell_id", methods=['GET'])
def mock_nef():
    #return handle_request('mock', 'get_mobile_cell_id', request=request)
    return handle_request('nef','get_mobile_cell_id', request=request)


if __name__ == '__main__':
    # app.run(ssl_context=("cert.pem","key.pem"),host=MEC_IP, port=MEC_IP_PORT) # https
    app.run(host=MEC_IP, port=MEC_IP_PORT)
