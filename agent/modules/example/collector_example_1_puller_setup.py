import hashlib
import logging
from datetime import datetime

from devocollectorsdk.inputs.collector_puller_setup_abstract import CollectorPullerSetupAbstract

log = logging.getLogger(__name__)


class CollectorExample1PullerSetup(CollectorPullerSetupAbstract):

    def setup(self, execution_timestamp: datetime):
        """

        :param execution_timestamp:
        :return:
        """

        log_message = "Starting the execution of setup()"
        log.debug(log_message)

        username = self.collector_variables["username"]
        password = self.collector_variables["password"]

        self.collector_variables["access_token"] = self._get_access_token(username, password)

        log_message = "Finalizing the execution of setup()"
        log.debug(log_message)

    @staticmethod
    def _get_access_token(username: str, password: str) -> str:
        return hashlib.sha256(f"{username}:{password}".encode("utf-8")).hexdigest()
