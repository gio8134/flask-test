import datetime
import hashlib
import os
import statistics

from config.module_context import MContext
from data_models.orchestrator_apps import OrchestratorResponse


class Orchestrator(object):

    def get_running_application(self, request, params):
        strategy = {
            'mock': MContext.mock.get_orchestrator_response,
            'tim_orchestrator': self.retrieve_running_application
        }
        function = strategy.get(os.environ['ORCHESTRATOR_MODE'], None)
        return OrchestratorResponse(function(request, params)).to_json()

    def retrieve_running_application(self, request, params=None):
        url = os.environ["ORCHESTRATOR_PROTOCOL"] + "://" + os.environ['ORCHESTRATOR_IP'] + ":" + str(os.environ['ORCHESTRATOR_PORT']) + "/admin/elo"

        headers = {
            'Content-Type': 'application/json',  # Set the content type to JSON
            'Accept': 'application/json'
        }
        return MContext.http_handler.perform_request(
            url=url,
            method='GET',
            headers=headers,
            params=params if params else request.args
        ).json()


