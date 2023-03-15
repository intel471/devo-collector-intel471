import logging
from datetime import datetime

from devocollectorsdk.inputs.collector_puller_setup_abstract import CollectorPullerSetupAbstract
from titan_client import ApiClient, Configuration, IndicatorsApi

log = logging.getLogger(__name__)


class Intel471IndicatorsPullerSetup(CollectorPullerSetupAbstract):

    def setup(self, execution_timestamp: datetime):
        """
        :param execution_timestamp:
        :return:
        """

        log.debug(f'Starting the execution of {self.name} -> setup()')

        username = self.collector_variables['username']
        password = self.collector_variables['password']

        configuration = Configuration(username=username, password=password)
        api_client = ApiClient(configuration)
        api_client.user_agent += '; Devo Intel 471 Malware Indicators Collector v1.0'
        api_instance = IndicatorsApi(api_client)

        self.collector_variables['api_instance'] = api_instance

        log.debug(f'Finalizing the execution of {self.name} -> setup()')
