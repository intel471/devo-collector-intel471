import hashlib
import logging
from datetime import datetime

from devocollectorsdk.inputs.collector_puller_setup_abstract import CollectorPullerSetupAbstract
from agent.modules.example.exceptions.exceptions import ExampleSetupException

log = logging.getLogger(__name__)


class CollectorExample10PullerSetup(CollectorPullerSetupAbstract):

    def setup(self, execution_timestamp: datetime):
        """

        :param execution_timestamp:
        :return:
        """

        if log.isEnabledFor(logging.DEBUG):
            log_message = "Starting the execution of setup()"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

        if "retry_counter" not in self.setup_variables:
            self.setup_variables["retry_counter"] = 0
        if self.setup_variables["retry_counter"] < 0:
            self.setup_variables["retry_counter"] += 1
            raise ExampleSetupException(0, "Error during setup process")

        username = self.collector_variables["username"]
        password = self.collector_variables["password"]

        self.collector_variables["access_token"] = self._get_access_token(username, password)

        if log.isEnabledFor(logging.DEBUG):
            log_message = f"Obtained an \"access_token\" value using \"username/password\" approach"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

        if log.isEnabledFor(logging.DEBUG):
            log_message = "Finalizing the execution of setup()"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

    def _get_access_token(self, username: str, password: str) -> str:
        if log.isEnabledFor(logging.DEBUG):
            log_message = f"Obtaining access token by username/password method"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")
        return hashlib.sha256(f"{username}:{password}".encode("utf-8")).hexdigest()
