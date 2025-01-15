class NefResponse(object):

    def __init__(self, nef_obj_json):
        self._nef_response_json = nef_obj_json
    
    @property
    def gnodeb_code(self)->str:
        return self._nef_response_json['gnodeb_code']
    
    @property
    def tracking_area(self)->str:
        return self._nef_response_json['tracking_area']
    
    @property
    def antenna_lat(self)->float:
        return self._nef_response_json['antenna_lat']
    
    @property
    def antenna_lon(self)->float:
        return self._nef_response_json['antenna_lon']

    def to_json(self):
        return self._nef_response_json
