import logging
from datetime import datetime
from typing import Dict, List

from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract
from devocollectorsdk.message.lookup_job_factory import LookupJobFactory
from titan_client.exceptions import ApiException, NotFoundException, UnauthorizedException

# noinspection PyUnresolvedReferences
from agent.modules.intel471.intel471_girs_puller_setup import Intel471GIRsPullerSetup
from agent.modules.intel471.exceptions.exceptions import *

log = logging.getLogger(__name__)

logging.getLogger('intel471_girs_puller').setLevel(logging.WARNING)


class Intel471GIRsPuller(CollectorPullerAbstract):

    def init_variables(
            self,
            input_config: dict,
            input_definition: dict,
            service_config: dict,
            service_definition: dict,
            module_config: dict,
            module_definition: dict,
            submodule_config: dict):
        """ Initialise variables """
        self.log_debug(f'{self.name} Starting the execution of init_variables()')

        # Initialization of properties from credentials section from configuration
        credentials: Dict[str, str] = input_config.get('credentials')
        if credentials is None:
            raise CredentialException(1, f'Missing required "credentials" section in the configuration')

        username: str = credentials.get('username')
        if username is None:
            raise CredentialException(2, f'Missing required "username" property from "credentials" section in configuration')
        self.collector_variables['username'] = username

        password: str = credentials.get('password')
        if password is None:
            raise CredentialException(3,'Missing required "password" property from "credentials" section in configuration')
        self.collector_variables['password'] = password

        self.collector_variables['api_params']: dict = {'count': 100, 'offset': 0}

        self.collector_variables['headers']: List[str] = ['gir_path', 'gir_name', 'gir_description']
        self.collector_variables['lookup_field_types']: List[str] = ['str', 'str', 'str']
        self.collector_variables['lookup_key']: str = 'gir_path'
        self.collector_variables['lookup_status']: str = None
        self.collector_variables['status']: bool = False

        self.log_debug(f'{self.name} Finalizing the execution of init_variables()')

    def pre_pull(self, retrieving_timestamp: datetime):
        """ Pre-pull method """
        self.log_info('[pre_pull] -> Creating relevant lookup_job_factory to be used by the pull method')

        self.collector_variables['gir_lookup_table']: LookupJobFactory = LookupJobFactory(
            lookup_name='general_intel_requirements',
            headers=self.collector_variables['headers'],
            field_types=self.collector_variables['lookup_field_types'],
            key=self.collector_variables['lookup_key'],
            historic_tag=self.collector_variables['lookup_status']
        )

        previous_state = self.persistence_object.load_state(no_log_traces=True)
        if previous_state:
            self.collector_variables['status'] = previous_state.get('status')

    def pull(self, retrieving_timestamp: datetime):
        """ Pull method """
        self.log_debug(f'Starting {self.name} pull()')

        total_girs = 0
        collected = 0

        api_instance = self.collector_variables['api_instance']
        params = self.collector_variables['api_params']

        try:
            api_response = api_instance.girs_get(**params)
            total_girs = api_response.gir_total_count
            girs = api_response.girs
            collected = len(girs)

            while collected < total_girs:
                params['offset'] += params['count']
                api_response = api_instance.girs_get(**params)
                girs.extend(api_response.girs)
                collected += len(api_response.girs)
        except UnauthorizedException:
            self.log_error(f'{self.__class__.__name__}[CODE:401] Unauthorised. Please check your TITAN credentials (email and API key) are configured correctly.')
        except NotFoundException:
            self.log_error(f'{self.__class__.__name__}[CODE:404] Not subscribed to this feed. Please contact your CSR to enquire about this feed.')
        except ApiException as e:
            if e.status == '429':
                self.log_error(f'{self.__class__.__name__}[CODE:429] Maximum API request limit hit. Please wait to try again or contact your CSR to increase limit if usage requires.')
            else:
                self.log_error(e)

        contents = self.girs_mappings(girs)

        self.send_to_devo(contents)  # Send data to Devo

        self.log_info(f'{total_girs} GIRs sent to output')

        self.log_debug('Saving state')
        state = {'status': self.collector_variables['status']}
        self.persistence_object.save_state(state, no_log_traces=True)
        self.log_debug('Saved state')

        self.log_debug('Finalizing pull()')

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def girs_mappings(self, girs: list):
        mappings = []
        for gir in girs:
            gir_data = gir.data.gir
            mappings.append([gir_data.path, gir_data.name, gir_data.description])
        return mappings

    def send_to_devo(self, content: list):
        """ Send data to Devo """
        # Checking status
        status: bool = self.collector_variables['status']
        lookup_job_factory: LookupJobFactory = self.collector_variables['gir_lookup_table']
        self.log_info(f'Status for {lookup_job_factory.lookup_name} -> {status}')

        if status:
            # Modify the table in Devo
            rejected, details = lookup_job_factory.add_item_to_list_to_modify(content)
            self.print_lookup_results(accepted=len(content) - rejected, rejected=rejected, details=details)
            self.send_lookup_messages(lookup_job_factory=lookup_job_factory, start=True, end=True, buffer='Modify')
            self.log_debug(f'Updated {lookup_job_factory.lookup_name} lookup table')
        else:
            # Create the table in Devo
            rejected, details = lookup_job_factory.add_item_to_list_to_initialize(content)
            self.print_lookup_results(accepted=len(content)-rejected, rejected=rejected, details=details)
            self.send_lookup_messages(lookup_job_factory=lookup_job_factory, start=True, end=True, buffer='Create')
            self.collector_variables['status'] = True
            self.log_debug(f'Created {lookup_job_factory.lookup_name} lookup table')

    def print_lookup_results(self, accepted: int, rejected: int, details: list):
        """ Print lookup results """
        total = accepted + rejected
        self.log_debug(f'Items sent to buffer: {total}')
        self.log_debug(f'Items accepted by Lookup Factory: {accepted}')
        self.log_debug(f'Items rejected by Lookup Factory: {rejected}')
        if rejected:
            self.log_debug(f'Rejected: {details}')
