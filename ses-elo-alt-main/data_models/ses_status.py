from enum import Enum


class StatusEnum(Enum):
    ON_GOING = 'ON-GOING'
    COMPLETED = 'COMPLETED-ACKNOWLEDGED'
    ERROR = 'ERROR'

class SESStatus(object):

    def __init__(self, ticket_request, process_status, results=None):
        self.ticket_request = ticket_request
        if not isinstance(process_status, StatusEnum):
            process_status = StatusEnum(process_status)
        self.process_status = process_status
        self.results = results


    def to_json(self):
        response_json = {
            'ticket_request': self.ticket_request,
            'process_status': self.process_status.value
        }
        if self.results:
            response_json['results'] = self.results
        return response_json