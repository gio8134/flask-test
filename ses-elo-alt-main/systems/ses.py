import os
import threading
import uuid

from config.module_context import MContext
from data_models.inventory_server import InventoryResponse
from data_models.ses_request import SESRequest
from data_models.ses_status import SESStatus, StatusEnum
from data_models.telemetry import MonitoringResponse, Telemetry


class SES(object):

    def __init__(self):
        self.request_db = dict()

    def trigger(self, request):
        strategy = {
            'mock': MContext.mock.ses_trigger,
            'poli': self.forward_to_poli,
            'tim': self.start_local_algo,
        }
        function = strategy.get(os.environ['SES_MODE'], None)
        response = function(request)
        return response

    def check_result(self, request):
        strategy = {
            'mock': MContext.mock.check_ses_result,
            'poli': self.forward_to_poli,
            'tim': self.check_algo_result,
        }
        function = strategy.get(os.environ['SES_MODE'], None)
        return function(request)

    def forward_to_poli(self, request):
        url = os.environ["POLI_PROTOCOL"] + "://" + os.environ['POLI_IP'] + ":" + str(
            os.environ['POLI_PORT']) + request.path
        return MContext.http_handler.perform_request(
            url=url,
            method=request.method,
            headers=request.headers,
            body=request.data
        ).json()

    def start_local_algo(self, request):
        ses_request = SESRequest(request.json)
        transaction_id = uuid.uuid4().hex
        self.request_db[transaction_id] = SESStatus(transaction_id, StatusEnum.ON_GOING)
        thread = threading.Thread(target=self.local_algo, args=(transaction_id, ses_request))
        thread.daemon = True  # Ensure the thread doesn't prevent the program from exiting
        thread.start()
        return self.request_db[transaction_id].to_json()

    def local_algo(self, transaction_id, ses_request):
        service_profile = ses_request.service_profile
        servers = InventoryResponse(MContext.inventory.get_inventory(None)).list_of_servers
        telemetry = MonitoringResponse(MContext.monitoring.get_kpi(None)).server_list
        indexed_telemetry = {
            t.server_id: t
            for t in telemetry
        }
        for srv in servers:
            if srv.server_id not in indexed_telemetry:
                indexed_telemetry[srv.server_id] = Telemetry({
                    "list_of_measurement": [{
                        "energy_consumption_KwH": 0,
                        "disk_usage_%": 0,
                        "gpu_usage_%": 0,
                        "ram_usage_%": 0,
                        "cpu_usage_%": 0}]})
        servers = list(filter(
            lambda s:
            s.cpu_equipped * (1 - indexed_telemetry[s.server_id].cpu_usage / 100) > service_profile.cpu_required and
            s.ram_capacity_mb * (
                    1 - indexed_telemetry[s.server_id].ram_usage / 100) > service_profile.ram_required_mb and
            (s.gpu_equipped < 0 or
            s.gpu_equipped * (1 - indexed_telemetry[s.server_id].gpu_usage / 100) >= service_profile.gpu_required) and
            s.disk_capacity_mb * (
                    1 - indexed_telemetry[s.server_id].disk_usage / 100) > service_profile.disk_required_mb,
            servers
        ))
        servers = sorted(servers,
                         key=lambda s: s.cpu_equipped * (1 - indexed_telemetry[s.server_id].cpu_usage / 100) +
                                       s.ram_capacity_mb / 1024 * (1 - indexed_telemetry[s.server_id].ram_usage / 100) +
                                       s.gpu_equipped * (1 - indexed_telemetry[s.server_id].gpu_usage / 100) +
                                       s.disk_capacity_mb / 1024 * (
                                                   1 - indexed_telemetry[s.server_id].disk_usage / 100))
        all_sites = list(set(s.site_id for s in servers))
        self.request_db[transaction_id].process_status = StatusEnum.COMPLETED
        self.request_db[transaction_id].results = list()
        if ses_request.site_required:
            servers = list(filter(lambda s: s.region_id == ses_request.region_required and
                                            s.site_id == ses_request.site_required,
                                  servers))
            if len(servers) == 0:
                raise ValueError(f'Placement not possible')
            best_server = servers[0]
            cluster_id = best_server.available_cluster_ids[0] if len(best_server.available_cluster_ids) > 0 else None
            self.request_db[transaction_id].results.append({
                "region_id": best_server.region_id,
                "site_id": best_server.site_id,
                "cluster_id": cluster_id,
                "server_id": best_server.server_id
            })

        if not ses_request.site_required and ses_request.region_required:
            servers = list(filter(lambda s: s.region_id == ses_request.region_required, servers))
            for site in all_sites:
                for server in servers:
                    if server.site_id == site:
                        best_server = server
                        cluster_id = best_server.available_cluster_ids[0] \
                            if len(best_server.available_cluster_ids) > 0 \
                            else None
                        self.request_db[transaction_id].results.append({
                            "region_id": best_server.region_id,
                            "site_id": best_server.site_id,
                            "cluster_id": cluster_id,
                            "server_id": best_server.server_id
                        })
                        break

        if not ses_request.site_required and not ses_request.region_required:
            for site in all_sites:
                for server in servers:
                    if server.site_id == site:
                        best_server = server
                        cluster_id = best_server.available_cluster_ids[0] \
                            if len(best_server.available_cluster_ids) > 0 \
                            else None
                        self.request_db[transaction_id].results.append({
                            "region_id": best_server.region_id,
                            "site_id": best_server.site_id,
                            "cluster_id": cluster_id,
                            "server_id": best_server.server_id
                        })
                        break

    def check_algo_result(self, request):
        transaction_id = request.args.get('transaction_id')
        return self.request_db[transaction_id].to_json()
