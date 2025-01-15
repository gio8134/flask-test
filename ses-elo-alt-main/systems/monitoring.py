import os

from config.module_context import MContext
from data_models.telemetry import MonitoringResponse


class Monitoring(object):

    def get_kpi(self, request):
        strategy = {
            'mock': MContext.mock.get_monitoring,
            'tim_platform': self.retrieve_from_tim,
            'eng_platform': self.retrieve_from_eng
        }
        function = strategy.get(os.environ['MONITORING_MODE'], None)
        return MonitoringResponse(function(request)).to_json()

    def retrieve_from_tim(self, request):
        url = os.environ["MONITORING_PROTOCOL"] + "://" + os.environ['MONITORING_IP'] + ":" + str(
            os.environ['MONITORING_PORT']) + "/v3/api/ses/get_network_kpi_trend"

        headers = {
            'Content-Type': 'application/json',  # Set the content type to JSON
            'Accept': 'application/json'
        }

        return MContext.http_handler.perform_request(
            url=url,
            method='GET',
            headers=headers
        ).json()

    def retrieve_from_eng(self, request):
        url = os.environ["MONITORING_PROTOCOL"] + "://" + os.environ['MONITORING_IP'] + ":" + str(
            os.environ['MONITORING_PORT']) + "/entity/find"

        headers = {
            'Content-Type': 'application/json',  # Set the content type to JSON
            'Accept': 'application/json'
        }
        body = {"type": "NODE", "name": "", "metricGroup": "TIM", "filters": []}
        return MContext.http_handler.perform_request(
            url=url,
            method='POST',
            headers=headers,
            body=body
        ).json()
