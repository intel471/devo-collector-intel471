import logging
from datetime import datetime, timedelta, timezone

from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract
from devocollectorsdk.message.lookup_job_factory import LookupJobFactory
from titan_client.exceptions import ApiException, NotFoundException, UnauthorizedException
from titan_client.models import IndicatorSearchSchema

# noinspection PyUnresolvedReferences
from agent.modules.intel471.intel471_indicators_puller_setup import Intel471IndicatorsPullerSetup
from agent.modules.intel471.exceptions.exceptions import *

log = logging.getLogger(__name__)

logging.getLogger('intel471_indicators_puller').setLevel(logging.WARNING)


class Intel471IndicatorsPuller(CollectorPullerAbstract):

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
        credentials: dict[str, str] = input_config.get('credentials')
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

        parameters: dict[str, int] = input_config.get('parameters')
        duration: int = parameters.get('duration_in_days')

        if duration is None:
            raise MissingDurationException(4, 'Missing "duration_in_days" value from "parameters" section in configuration')
        elif not isinstance(duration, int):
            raise InvalidDurationException(5, '"duration_in_days" value must be of "int" type')
        elif duration < 1:
            raise InvalidDurationException(6, '"duration_in_days" value must be >= 1')

        self.collector_variables['api_params']: dict = {'count': 100, '_from': self.get_from_timestamp(duration)}

        if service_config and 'request_period_in_seconds' in service_config:
            raise DefaultsOverrideException(7, 'Default "request_period_in_seconds" cannot be overridden')

        base_headers: list[str] = [
            'uid',
            'first_seen',
            'last_seen',
            'indicator_type',
            'context',
            'malware_family',
            'malware_family_version',
            'malware_family_variant',
            'expiration',
            'confidence',
            'mitre_tactics',
            'gir'
        ]

        self.collector_variables['file_lookup_headers']: list[str] = base_headers + [
            'download_url',
            'md5',
            'sha1',
            'sha256',
            'ssdeep',
            'size',
            'type'
        ]
        self.collector_variables['file_lookup_field_types']: list[str] = ['str'] * len(self.collector_variables['file_lookup_headers'])
        self.collector_variables['file_lookup_field_types'][-2] = 'int4'

        self.collector_variables['ipv4_lookup_headers']: list[str] = base_headers + [
            'ip_address',
            'isp',
            'city',
            'country'
        ]
        self.collector_variables['ipv4_lookup_field_types']: list[str] = ['str'] * len(self.collector_variables['ipv4_lookup_headers'])
        self.collector_variables['ipv4_lookup_field_types'][len(base_headers)] = 'ip4'  # set ip_address field type to ip4

        self.collector_variables['url_lookup_headers']: list[str] = base_headers + ['url']
        self.collector_variables['url_lookup_field_types']: list[str] = ['str'] * len(self.collector_variables['url_lookup_headers'])

        self.collector_variables['lookup_key']: str = 'uid'
        self.collector_variables['lookup_status']: str = None

        self.collector_variables['status']: list[str, bool] = {'file': False, 'ipv4': False, 'url': False}

        self.log_debug(f'{self.name} Finalizing the execution of init_variables()')

    def pre_pull(self, retrieving_timestamp: datetime):
        """ Pre-pull method """
        self.log_info('[pre_pull] -> Creating relevant lookup_job_factory to be used by the pull method')

        file_lookup_table: LookupJobFactory = LookupJobFactory(
            lookup_name='malicious_file',
            headers=self.collector_variables['file_lookup_headers'],
            field_types=self.collector_variables['file_lookup_field_types'],
            key=self.collector_variables['lookup_key'],
            historic_tag=self.collector_variables['lookup_status']
        )

        ipv4_lookup_table: LookupJobFactory = LookupJobFactory(
            lookup_name='malicious_ipv4',
            headers=self.collector_variables['ipv4_lookup_headers'],
            field_types=self.collector_variables['ipv4_lookup_field_types'],
            key=self.collector_variables['lookup_key'],
            historic_tag=self.collector_variables['lookup_status']
        )

        url_lookup_table: LookupJobFactory = LookupJobFactory(
            lookup_name='malicious_url',
            headers=self.collector_variables['url_lookup_headers'],
            field_types=self.collector_variables['url_lookup_field_types'],
            key=self.collector_variables['lookup_key'],
            historic_tag=self.collector_variables['lookup_status']
        )

        self.collector_variables['lookup_tables'] = {
            'file': file_lookup_table,
            'ipv4': ipv4_lookup_table,
            'url': url_lookup_table,
        }

        previous_state = self.persistence_object.load_state(no_log_traces=True)
        if previous_state:
            self.collector_variables['api_params']['cursor'] = previous_state.get('cursor')
            self.collector_variables['status'] = previous_state.get('status')

    def pull(self, retrieving_timestamp: datetime):
        """ Pull method """
        self.log_debug(f'Starting {self.name} pull()')

        total_indicators = 0
        expired = 0
        contents = {'file': [], 'ipv4': [], 'url': []}

        api_instance = self.collector_variables['api_instance']
        params = self.collector_variables['api_params']

        try:
            while True:
                api_response = api_instance.indicators_stream_get(**params)
                if not api_response.indicators:
                    state = {'cursor': params['cursor']}
                    break
                total_indicators += len(api_response.indicators)
                for indicator in api_response.indicators:
                    # Only parse and send unexpired indicators
                    if indicator.data.expiration > int(datetime.now(timezone.utc).timestamp() * 1000):
                        type, content = self.parse_indicator(indicator)
                        contents[type].append(content)
                    else:
                        expired += 1
                params['cursor'] = api_response.cursor_next
        except UnauthorizedException:
            self.log_error(f'{self.__class__.__name__}[CODE:401] Unauthorised. Please check your TITAN credentials (email and API key) are configured correctly.')
        except NotFoundException:
            self.log_error(f'{self.__class__.__name__}[CODE:404] Not subscribed to this feed. Please contact your CSR to enquire about this feed.')
        except ApiException as e:
            if e.status == '429':
                self.log_error(f'{self.__class__.__name__}[CODE:429] Maximum API request limit hit. Please wait to try again or contact your CSR to increase limit if usage requires.')
            else:
                self.log_error(e)

        [self.send_to_devo(content, type) for type, content in contents.items() if content]  # Send data to Devo

        self.log_info(f'{total_indicators} indicators sent to output')
        self.log_info(f'{expired} indicators not sent to output because expired')
        self.log_info(f"{len(contents['file'])} file indicators, {len(contents['ipv4'])} ipv4 indicators, {len(contents['url'])} url indicators")

        self.log_debug('Saving state')
        state['status'] = self.collector_variables['status']
        self.persistence_object.save_state(state, no_log_traces=True)
        self.log_debug('Saved state')

        self.log_debug('Finalizing pull()')

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def get_from_timestamp(self, ndays: int) -> int:
        """ Generate _from timestamp """
        now = datetime.now(tz=timezone.utc)
        today = datetime(year=now.year, month=now.month, day=now.day, tzinfo=timezone.utc)
        return int((today - timedelta(days=ndays)).timestamp() * 1000)

    def get_readable_date(self, epoch: int) -> str:
        """ Convert epoch timestamp into human readable date """
        return datetime.fromtimestamp(epoch / 1000).strftime('%-d %b %Y')

    def parse_indicator(self, indicator: IndicatorSearchSchema) -> int:
        """ Parse indicators for relevant data to send to Devo """
        try:
            indicator_type = indicator.data.indicator_type
            indicator_data = indicator.data.indicator_data

            malware_data = indicator.data.threat.data
            malware_family = malware_data.family
            malware_variant = malware_data.variant if malware_data.variant else 'n/a'
            malware_version = malware_data.version if malware_data.version else 'n/a'

            content = [
                indicator.uid,
                self.get_readable_date(indicator.activity.first),
                self.get_readable_date(indicator.activity.last),
                indicator_type,
                indicator.data.context.description,
                malware_family,
                malware_version,
                malware_variant,
                self.get_readable_date(indicator.data.expiration),
                indicator.data.confidence,
                indicator.data.mitre_tactics,
                ' / '.join(indicator.data.intel_requirements),
            ]

            if indicator_type == 'file':
                content += [
                    indicator_data.file.download_url,
                    indicator_data.file.md5,
                    indicator_data.file.sha1,
                    indicator_data.file.sha256,
                    indicator_data.file.ssdeep,
                    indicator_data.file.size,
                    indicator_data.file.type,
                ]
            elif indicator_type == 'ipv4':
                geo_ip = indicator_data.geo_ip
                if geo_ip:
                    content += [
                        indicator_data.address,
                        geo_ip.isp.isp,
                        geo_ip.city if geo_ip.city else 'n/a',
                        geo_ip.country,
                    ]
                else:
                    content += [indicator_data.address, 'n/a', 'n/a', 'n/a']
            elif indicator_type == 'url':
                content += [indicator_data.url]

            return indicator_type, content
        except AttributeError as e:
            self.log_error(f'Indicator with UID = {indicator.uid} encountered the following exception {e}')

    def send_to_devo(self, content: list, indicator_type: str):
        """ Send data to Devo """
        # Checking status
        status: bool = self.collector_variables['status'][indicator_type]
        lookup_job_factory: LookupJobFactory = self.collector_variables['lookup_tables'][indicator_type]
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
            self.collector_variables['status'][indicator_type] = True
            self.log_debug(f'Created {lookup_job_factory.lookup_name} lookup table')

    def print_lookup_results(self, accepted: int, rejected: int, details: list):
        """ Print lookup results """
        total = accepted + rejected
        self.log_debug(f'Items sent to buffer: {total}')
        self.log_debug(f'Items accepted by Lookup Factory: {accepted}')
        self.log_debug(f'Items rejected by Lookup Factory: {rejected}')
        if rejected:
            self.log_debug(f'Rejected: {details}')
