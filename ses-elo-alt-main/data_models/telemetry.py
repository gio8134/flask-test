class Telemetry(object):

    def __init__(self, telemetry_json):
        self._telemetry_json = telemetry_json

    @property
    def server_id(self):
        return self._telemetry_json['server_id']

    @property
    def last_measurement(self):
        return self._telemetry_json['list_of_measurement'][-1]

    @property
    def disk_usage(self):
        return self.last_measurement['disk_usage_%']

    @property
    def gpu_usage(self):
        return self.last_measurement['gpu_usage_%']

    @property
    def ram_usage(self):
        return self.last_measurement['ram_usage_%']

    @property
    def cpu_usage(self):
        return self.last_measurement['cpu_usage_%']


class MonitoringResponse(object):

    def __init__(self, monitoring_json):
        self._monitoring_json = monitoring_json

    @property
    def server_list(self):
        return [Telemetry(s) for s in self._monitoring_json.get('server_list', list())]

    def to_json(self):
        return self._monitoring_json
