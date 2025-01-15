class Context(object):

    def __init__(self):
        self._ses = None
        self._elo = None
        self._inventory = None
        self._monitoring = None
        self._orchestrator = None
        self._mock = None
        self._http_handler = None
        self._nef = None

    @property
    def nef(self):
        if self._nef is None:
            from systems.nef import nef
            self._nef = nef()
        return self._nef

    @property
    def ses(self):
        if self._ses is None:
            from systems.ses import SES
            self._ses = SES()
        return self._ses

    @property
    def elo(self):
        if self._elo is None:
            from systems.elo import ELO
            self._elo = ELO()
        return self._elo

    @property
    def inventory(self):
        if self._inventory is None:
            from systems.inventory import Inventory
            self._inventory = Inventory()
        return self._inventory

    @property
    def monitoring(self):
        if self._monitoring is None:
            from systems.monitoring import Monitoring
            self._monitoring = Monitoring()
        return self._monitoring

    @property
    def orchestrator(self):
        if self._orchestrator is None:
            from systems.orchestrator import Orchestrator
            self._orchestrator = Orchestrator()
        return self._orchestrator

    @property
    def mock(self):
        if self._mock is None:
            from systems.mock_class import Mock
            self._mock = Mock()
        return self._mock

    @property
    def http_handler(self):
        if self._http_handler is None:
            from systems.http_handler import HTTPHandler
            self._http_handler = HTTPHandler()
        return self._http_handler

MContext = Context()