from config.module_context import MContext
from data_models import mocked_responses
import threading, time
import uuid

from data_models.ses_status import SESStatus, StatusEnum


class Mock(object):

    def __init__(self):
        self.ses_request_db = dict()
        self.threads = dict()

    def ses_trigger(self, request):
        transaction_id = uuid.uuid4().hex
        thread = threading.Thread(target=self.ses_mock_task, args=(transaction_id,))
        self.threads[transaction_id] = thread
        thread.daemon = True  # Ensure the thread doesn't prevent the program from exiting
        thread.start()
        response = mocked_responses.new_ses_trigger
        response['ticket_request'] = transaction_id
        MContext.mock.ses_request_db[transaction_id] = SESStatus(transaction_id, StatusEnum.ON_GOING)
        return response

    def ses_mock_task(self, transaction_id):
        time.sleep(10)  # Simulate work
        self.ses_request_db[transaction_id].process_status = StatusEnum.COMPLETED
        self.ses_request_db[transaction_id].results = mocked_responses.ses_result_completed['results']

    def elo_analysis(self, request):
        return mocked_responses.elo_result

    def check_ses_result(self, request):
        transaction_id = request.args.get('transaction_id')
        return self.ses_request_db[transaction_id].to_json()

    def get_inventory(self, request):
        return mocked_responses.inventory

    def get_monitoring(self, request):
        return mocked_responses.monitoring

    def get_netbox_response(self, request):
        return mocked_responses.netbox_response

    def get_tim_monitoring_response(self, request):
        return mocked_responses.tim_monitoring_response

    def get_orchestrator_response(self, request, params=None):
        return mocked_responses.tim_orchestrator_response

    def get_mobile_cell_id(self, request):
        return mocked_responses.nef_response
