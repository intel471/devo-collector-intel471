import logging
from datetime import datetime

from devocollectorsdk.inputs.collector_puller_setup_abstract import CollectorPullerSetupAbstract

log = logging.getLogger(__name__)


class CollectorExample6PullerSetup(CollectorPullerSetupAbstract):

    def setup(self, execution_timestamp: datetime):
        """

        :param execution_timestamp:
        :return:
        """

        self.log_debug("Starting the execution of setup()")

        self.log_debug("Finalizing the execution of setup()")
