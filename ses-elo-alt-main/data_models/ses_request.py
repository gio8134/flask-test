class ServiceProfile(object):

    def __init__(self, service_profile_json):
        self._service_profile_json = service_profile_json

    @property
    def disk_required_mb(self):
        return self._service_profile_json['disk_required_MB']

    @property
    def gpu_required(self):
        return self._service_profile_json['GPU_required']

    @property
    def ram_required_mb(self):
        return self._service_profile_json['RAM_required_MB']

    @property
    def cpu_required(self):
        return self._service_profile_json['vCPU_required']


class SESRequest(object):

    def __init__(self, request_json):
        self._request_json = request_json

    @property
    def service_profile(self):
        return ServiceProfile(self._request_json['service_profile'])

    @property
    def region_required(self):
        return self._request_json['location']['region_id']
    @property
    def site_required(self):
        return self._request_json['location']['site_id']