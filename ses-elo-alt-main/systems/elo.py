import os

import requests
import haversine as hs

from config.module_context import MContext
from data_models.inventory_server import InventoryResponse
from data_models.orchestrator_apps import OrchestratorResponse


class ELO(object):

    def __init__(self):
        pass

    def trigger(self, request):
        strategy = {
            'mock': MContext.mock.elo_analysis,
            'tim': self.compute_nearest
        }
        function = strategy.get(os.environ['ELO_MODE'], None)
        return function(request)

    def compute_nearest(self, request):
        user_cell = MContext.mock.get_mobile_cell_id(request)
        user_position = (user_cell['antenna_lat'], user_cell['antenna_lon'])
        params = {'app_id': request.json.get('app_id')}
        servers = InventoryResponse(MContext.inventory.get_inventory(request)).list_of_servers
        indexed_servers = {
            s.server_id: s
            for s in servers
        }
        orchestrator_apps = OrchestratorResponse(MContext.orchestrator.get_running_application(request, params))
        running_apps = orchestrator_apps.list_of_images
        if len(running_apps) == 0:
            raise ValueError(f'No valid server found with running app')
        running_apps = sorted(running_apps, key=lambda app: hs.haversine(user_position,
                                                                         (indexed_servers[app.server_id].latitude,
                                                                          indexed_servers[app.server_id].longitude)))
        return {
            "elo_analysis_outcome": {
                "server_id": running_apps[0].server_id,
                "ip_address": running_apps[0].endpoint,
                "app_mean_deployment_time_seconds": orchestrator_apps.app_mean_deployment_time_seconds
            }
        }
