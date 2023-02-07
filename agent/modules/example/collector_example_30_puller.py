import logging
from datetime import datetime

from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract
from devocollectorsdk.message.lookup_job_factory import LookupJobFactory

log = logging.getLogger(__name__)


class CollectorExample30Puller(CollectorPullerAbstract):

    # def create_setup_instance(
    #         self,
    #         setup_class_name: str,
    #         autosetup_enabled: bool,
    #         collector_variables: dict) -> CollectorPullerSetupAbstract:
    #     pass

    def init_variables(self,
                       input_config: dict,
                       input_definition: dict,
                       service_config: dict,
                       service_definition: dict,
                       module_config: dict,
                       module_definition: dict,
                       submodule_config: dict):

        log.info('[init_variables] -> Pushing values to collector_variables object')
        self.collector_variables['lookup_name']: str = 'example_puller_30'
        self.collector_variables["lookup_headers"]: [str] = ['uuid', 'username', 'last_ip']
        self.collector_variables["lookup_field_types"]: [str] = ['str', 'str', 'ip4']
        self.collector_variables["lookup_key"]: [str] = 'uuid'
        self.collector_variables['lookup_status']: [str] = None

        self.collector_variables['content_to_create'] = [
            ['001', 'Pablo', '192.168.1.1'],
            ['002', 'Carlos', '192.168.1.2'],
            ['003', 'Felipe', '192.168.1.3'],
            ['004', 'Javier', 'internal-node-004'],
        ]

        self.collector_variables['content_to_modify'] = [
            ['004', 'Javier', '192.168.1.4'],
        ]

        self.collector_variables['content_to_remove'] = [
            ['001'],
            ['002'],
            ['003'],
            ['004'],
        ]

    def pre_pull(self, retrieving_timestamp: datetime):

        log.info('[pre_pull] -> Creating a new lookup_job_factory to be used by the pull method')

        lookup_job_factory_1: LookupJobFactory = LookupJobFactory(
            lookup_name=self.collector_variables['lookup_name'],
            headers=self.collector_variables["lookup_headers"],
            field_types=self.collector_variables["lookup_field_types"],
            key=self.collector_variables["lookup_key"],
            historic_tag=self.collector_variables['lookup_status']
        )

        self.collector_variables['lookup_job_factory_1']: LookupJobFactory = lookup_job_factory_1

    def pull(self, retrieving_timestamp: datetime):

        # Checking status
        status = self.collector_variables.get('status')
        log.info(f"Status -> {status}")

        # Get the lookup_job_factory
        lookup_job_factory_1: LookupJobFactory = self.collector_variables['lookup_job_factory_1']

        if status is None:

            # Create the table in Devo
            content = self.collector_variables['content_to_create']
            rejected, details = lookup_job_factory_1.add_item_to_list_to_initialize(content)
            self.__print_lookup_results(accepted=len(content)-rejected, rejected=rejected)

            self.send_lookup_messages(lookup_job_factory=lookup_job_factory_1, start=True, end=True, buffer='Create')

            self.collector_variables['status']: str = 'CREATED_LOOKUP_TABLE'
            log.info(f"New status -> {self.collector_variables['status']}")

        elif status == 'CREATED_LOOKUP_TABLE':

            # Modify the table in Devo
            content = self.collector_variables['content_to_modify']
            rejected, details = lookup_job_factory_1.add_item_to_list_to_modify(content)
            self.__print_lookup_results(accepted=len(content) - rejected, rejected=rejected)

            self.send_lookup_messages(lookup_job_factory=lookup_job_factory_1, start=True, end=True, buffer='Modify')

            self.collector_variables['status']: str = 'MODIFIED_LOOKUP_TABLE'
            log.info(f"New status -> {self.collector_variables['status']}")

        else:

            # Remove the table in Devo
            content = self.collector_variables['content_to_remove']
            rejected, details = lookup_job_factory_1.add_item_to_list_to_remove(content)
            self.__print_lookup_results(accepted=len(content) - rejected, rejected=rejected)

            self.send_lookup_messages(lookup_job_factory=lookup_job_factory_1, start=True, end=True, buffer='Remove')

            self.collector_variables['status']: str = 'REMOVED_LOOKUP_TABLE'
            log.info(f"New status -> {self.collector_variables['status']}")

            # Terminate collector
            log.info("Demo job has been completed")
            log.info("running_flag has been updated to False")
            self.running_flag = False

    @staticmethod
    def __print_lookup_results(accepted: int, rejected: int):
        """
        Print lookup results
        @param accepted: Number of accepted items.
        @param rejected: Number of rejected items.
        """
        total = accepted + rejected
        log.info(f'Items sent to buffer: {total}')
        log.info(f'Items accepted by Lookup Factory: {accepted}')
        log.info(f'Items rejected by Lookup Factory: {rejected}')

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass
