class Server(object):

    def __init__(self, server_json):
        self._server_json = server_json

    @property
    def server_id(self):
        return self._server_json['server_id']

    @property
    def latitude(self):
        return self._server_json['coordinates']['latitude']

    @property
    def longitude(self):
        return self._server_json['coordinates']['longitude']

    @property
    def site_id(self):
        return self._server_json['site_id']

    @property
    def region_id(self):
        return self._server_json['region_id']

    @property
    def hw_list(self):
        return self._server_json['HW_list']

    @property
    def cpu_equipped(self):
        return self.hw_list['CPU_equipped']

    @property
    def disk_capacity_mb(self):
        return self.hw_list['Disk_capacity_MB']

    @property
    def gpu_equipped(self):
        return self.hw_list['GPU_equipped']

    @property
    def ram_capacity_mb(self):
        return self.hw_list['RAM_capacity_MB']

    @property
    def available_cluster_ids(self):
        return [c['cluster_id'] for c in self._server_json['cluster_list']]

class InventoryResponse(object):

    def __init__(self, inventory_json):
        self._inventory_json = inventory_json

    @property
    def list_of_servers(self):
        return [Server(s) for s in self._inventory_json.get('list_of_server', list())]

    def to_json(self):
        return self._inventory_json