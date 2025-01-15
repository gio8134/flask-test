import requests
import json
import traceback
import os

from data_models.nef_response import NefResponse
from config.module_context import MContext

class nef(object):

    def get_mobile_cell_id(self, request):
        strategy = {
            'mock': MContext.mock.get_mobile_cell_id,
            'network': self.get_cell_from_network_nef_service
        }
        function = strategy.get(os.environ['NEF_MODE'], None)
        return NefResponse(function(request)).to_json()

    def get_cell_from_network_nef_service(self, request):
        serving_cell_descriptor = {}
        url_nef = os.environ['NEF_PROTOCOL']+"://"+os.environ['NEF_IP']+":"+str(os.environ['NEF_PORT'])
        URL = url_nef+"/api/elo/v1/nef_translate_mobile_ip_to_cell_id"
        PARAMS = { 
            "lat_mobile": 45.4,
            "lon_mobile":9.7
        } 
        try:
            r = requests.get(url = URL, params=PARAMS)
            serving_cell_descriptor = json.loads(r.content)
        except Exception as e1:
            print(e1)
            print(traceback.format_exc())
            return { 'error':'nef service: cell not found' }
        return serving_cell_descriptor