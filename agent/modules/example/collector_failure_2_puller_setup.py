import hashlib
import logging
import random
from datetime import datetime

from devocollectorsdk.inputs.collector_puller_setup_abstract import CollectorPullerSetupAbstract

log = logging.getLogger(__name__)


class CollectorFailure2PullerSetup(CollectorPullerSetupAbstract):

    def setup(self, execution_timestamp: datetime):
        """

        :param execution_timestamp:
        :return:
        """

        log_message = "Starting the execution of setup()"
        log.debug(log_message)

        random_error = random.choice([1, 1, 1, 0])
        if random_error == 1:
            raise RuntimeError('Error Time on setup')

        log_message = "Finalizing the execution of setup()"
        log.debug(log_message)

    @staticmethod
    def _get_access_token(username: str, password: str) -> str:
        return hashlib.sha256(f"{username}:{password}".encode("utf-8")).hexdigest()
