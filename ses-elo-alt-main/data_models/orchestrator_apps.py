class RunningInstance(object):

    def __init__(self, running_instance_json):
        self._running_instance_json = running_instance_json

    @property
    def server_id(self):
        return self._running_instance_json['server_id']

    @property
    def endpoint(self):
        return self._running_instance_json['DNS']


class OrchestratorResponse(object):

    def __init__(self, orchestrator_json):
        self._orchestrator_json = orchestrator_json

    @property
    def list_of_images(self):
        return [RunningInstance(a) for a in self._orchestrator_json.get('list_of_images', list())]

    @property
    def app_mean_deployment_time_seconds(self):
        return self._orchestrator_json['app_mean_deployment_time_seconds']

    def to_json(self):
        return self._orchestrator_json
