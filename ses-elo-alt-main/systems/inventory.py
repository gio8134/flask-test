import datetime
import hashlib
import os
import statistics

from data_models.inventory_server import InventoryResponse
from config.module_context import MContext


class Inventory(object):

    def get_inventory(self, request):
        strategy = {
            'mock': MContext.mock.get_inventory,
            'netbox': self.retrieve_inventory_from_netbox
        }
        function = strategy.get(os.environ['INVENTORY_MODE'], None)
        return InventoryResponse(function(request)).to_json()

    def retrieve_inventory_from_netbox(self, request):
        url = os.environ["INVENTORY_PROTOCOL"] + "://" + os.environ['INVENTORY_IP'] + ":" + str(os.environ['INVENTORY_PORT']) + "/graphql/"

        headers = {
            'Authorization': f'Token {os.environ["INVENTORY_TOKEN"]}',  # Add the token to the Authorization header
            'Content-Type': 'application/json',  # Set the content type to JSON
            'Accept': 'application/json'
        }
        query = {"query":"{\n  device_list(filters: { tag: \"edge\" }) {\n    name\n    site {\n      latitude\n      longitude\n      slug\n      region {\n        slug\n      }\n    }\n    tenant {\n      slug\n    }\n    cluster {\n      name\n    }\n    last_updated\n    modules {\n      display\n      custom_fields\n    }\n    powerports {\n      custom_fields\n    }\n  }\n}"}
        netbox_response = MContext.http_handler.perform_request(
            url=url,
            method='POST',
            headers=headers,
            body=query,
            other_args={'verify': False}
        ).json()
        output_structure = dict()
        timestamp = int(datetime.datetime.now().timestamp())
        # Convert the integer timestamp to a datetime object
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        iso_formatted_string = dt_object.isoformat()
        output_structure['inventory_timestamp'] = iso_formatted_string
        output_structure['list_of_server'] = list()
        for device in netbox_response['data']['device_list']:
            output_structure['list_of_server'].append({
                "server_id": device['name'],
                "HW_list": {
                    "CPU_equipped": sum(module['custom_fields']['cores'] for module in device['modules']),
                    "cost_per_CPU": 1,
                    "Disk_capacity_MB": 1024 * sum(
                        module['custom_fields']['disk_capacity_GB'] for module in device['modules']),
                    "cost_Disk_per_MB": 1,
                    "GPU_equipped": len(list(module['custom_fields']['gpu_memory_GB'] for module in device['modules'] if
                                             module['custom_fields']['gpu_memory_GB'] > 0)),
                    "cost_GPU_per_MB": 1,
                    "RAM_capacity_MB": 1024 * sum(
                        module['custom_fields']['ram_capacity_GB'] for module in device['modules']),
                    "cost_RAM_per_MB": 1,
                },
                "site_id": device['site']['slug'],
                "region_id": device['site']['region']['slug'],
                "coordinates": {
                    "latitude": float(device['site']['latitude']),
                    "longitude": float(device['site']['longitude'])
                },
                "green_power_percentage": statistics.mean(
                    module['custom_fields']['GreenPowerPercentage'] for module in device['powerports']),
                # "green_power_percentage":20,
                "CO2_emission": (int(hashlib.sha256(device['name'].encode('utf-8')).hexdigest(), 16) % 10 ** 8) % 100,
                # use hash function to make it random but always the same based on the server
                # "last_inventory_get_timestamp": int(datetime.datetime.fromisoformat(device['last_updated']).timestamp()),
                "last_inventory_get_timestamp": iso_formatted_string,
                "cluster_list": [
                    {"cluster_id": device['cluster']['name']}
                ] if device['cluster'] is not None else []
            })

        return output_structure

