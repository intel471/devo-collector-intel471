import hashlib
import logging
from datetime import datetime

from devocollectorsdk.inputs.collector_puller_setup_abstract import CollectorPullerSetupAbstract
from agent.modules.example.exceptions.exceptions import ExampleSetupException

log = logging.getLogger(__name__)


class CollectorExample12PullerSetup(CollectorPullerSetupAbstract):

    def setup(self, execution_timestamp: datetime):
        """

        :param execution_timestamp:
        :return:
        """

        if log.isEnabledFor(logging.DEBUG):
            log_message = "Starting the execution of setup()"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

        if log.isEnabledFor(logging.DEBUG):
            log_message = "Finalizing the execution of setup()"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")
