import json
import logging
from datetime import datetime

# noinspection PyUnresolvedReferences
from agent.modules.example.collector_example_11_puller_setup import CollectorExample11PullerSetup
from agent.modules.example.commons.commons import MockRequest, Utils, MockResponse
from agent.modules.example.exceptions.exceptions import ExampleException
from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract

log = logging.getLogger(__name__)

logging.getLogger("faker.factory").setLevel(logging.WARNING)


class CollectorExample11Puller(CollectorPullerAbstract):
    COLLECTOR_VERSION = 1

    # def create_setup_instance(
    #         self,
    #         setup_class_name: str,
    #         autosetup_enabled: bool,
    #         collector_variables: dict) -> CollectorPullerSetupAbstract:
    #
    #     setup_class = globals()[setup_class_name]
    #     return setup_class(
    #         self,
    #         collector_variables,
    #         autosetup_enabled,
    #         self.input_id,
    #         self.input_name,
    #         self.input_config,
    #         self.input_definition,
    #         self.service_name,
    #         self.service_type,
    #         self.service_config,
    #         self.service_definition,
    #         self.module_name,
    #         self.module_config,
    #         self.module_definition,
    #         self.persistence_object,
    #         self.output_queue,
    #         self.submodule_name,
    #         self.submodule_config
    #     )

    def init_variables(
            self,
            input_config: dict,
            input_definition: dict,
            service_config: dict,
            service_definition: dict,
            module_config: dict,
            module_definition: dict,
            submodule_config: dict):
        """

        :param input_config:
        :param input_definition:
        :param service_config:
        :param service_definition:
        :param module_config:
        :param module_definition:
        :param submodule_config:
        :return:
        """

        if log.isEnabledFor(logging.DEBUG):
            log_message = f"{self.getName()} Starting the execution of init_variables()"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

        # Initialization of properties from credentials section from configuration
        credentials_section = input_config.get("credentials")
        if credentials_section:
            username = credentials_section.get("username")
            if username:
                self.collector_variables["username"] = username
            else:
                raise ExampleException(
                    0, "Missing required \"username\" property from \"credentials\" section in configuration"
                )

            password = credentials_section.get("password")
            if password:
                self.collector_variables["password"] = password
            else:
                raise ExampleException(
                    1, "Missing required \"password\" property from \"credentials\" section in configuration"
                )
        else:
            raise ExampleException(
                3, "Missing required \"credentials\" section in the configuration"
            )

        # Initialization of properties from module_properties section from definitions file
        module_properties = module_definition.get("module_properties")
        if module_properties:
            base_url: str = module_properties.get("base_url")
            if base_url:
                self.collector_variables["base_url"] = base_url
            else:
                raise ExampleException(
                    4, "Missing required \"base_url\" property from \"module_properties\" "
                       "section in collector definitions"
                )

            base_tag: str = module_properties.get("base_tag")
            if base_tag:
                self.collector_variables["base_tag"] = base_tag
            else:
                raise ExampleException(
                    5, "Missing required \"base_tag\" property from \"module_properties\" "
                       "section in collector definitions"
                )

            max_number_of_messages_per_page: int = module_properties.get("max_number_of_messages_per_page")
            if max_number_of_messages_per_page:
                self.collector_variables["max_number_of_messages_per_page"] = max_number_of_messages_per_page
            else:
                raise ExampleException(
                    6,
                    "Missing required \"max_number_of_messages_per_page\" property "
                    "from \"module_properties\" section in collector definitions"
                )

        else:
            raise ExampleException(7, "Missing required \"module_properties\" "
                                      "section in the collector definitions")

        # Getting a property from the configuration (if exists)
        if "max_number_of_messages_per_page" in service_config:
            self.collector_variables["max_number_of_messages_per_page"]: int = \
                service_config["max_number_of_messages_per_page"]

        self.collector_variables["region"] = submodule_config
        self.collector_variables["key1"] = "value1"

        if log.isEnabledFor(logging.DEBUG):
            log_message = f"{self.getName()} Finalizing the execution of init_variables()"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

    def pre_pull(self, retrieving_timestamp: datetime):
        """Not required for this collector

        :param retrieving_timestamp:
        :return:
        """
        pass

    def pull(self, retrieving_timestamp: datetime):
        """

        :param retrieving_timestamp:
        :return:
        """

        if log.isEnabledFor(logging.DEBUG):
            log_message = "Starting pull()"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

        # It is recommended to send some stats info to output

        start_time_overall = datetime.utcnow()

        requests_counter, received_messages_counter, removed_messages_counter, generated_messages_counter, tag_used = \
            self._get_data_and_send_to_devo(retrieving_timestamp)

        elapsed_time_overall = (datetime.utcnow() - start_time_overall).total_seconds()
        elapsed_time_per_message_overall = (elapsed_time_overall / received_messages_counter) * 1000 \
            if received_messages_counter > 0 else elapsed_time_overall

        if log.isEnabledFor(logging.INFO):
            log_message = \
                f"Number of requests {requests_counter}, " \
                f"received {received_messages_counter} message(s), " \
                f"removed {removed_messages_counter} message(s), " \
                f"generated and sent {generated_messages_counter} message(s), " \
                f"tag used: \"{tag_used}\". " \
                f"avg_time_per_source_message: {elapsed_time_per_message_overall:0.3f} ms"
            log.info(log_message)
            self.send_internal_collector_message(log_message, level="info")

        if log.isEnabledFor(logging.DEBUG):
            log_message = "Finalizing pull()"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

    def _get_data_and_send_to_devo(self, retrieving_timestamp: datetime) -> (int, int, int, int, str):
        """

        :param retrieving_timestamp:
        :return:
        """

        max_number_of_messages_per_page: int = self.collector_variables["max_number_of_messages_per_page"]

        # Recover the persisted data information
        persisted_info = self._get_persisted_data_info()

        if log.isEnabledFor(logging.DEBUG):
            log_message = f"Previous persisted info: {persisted_info}"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

        # Calculates the tag value
        tag: str = self._prepare_tag()

        if log.isEnabledFor(logging.DEBUG):
            log_message = f"The tag \"{tag}\" will be used for sending the messages"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

        access_token: str = self.collector_variables["access_token"]

        # Creation of initial URL, it will be used the persisted data information
        first_url: str = self._create_first_url(retrieving_timestamp, persisted_info=persisted_info)

        if log.isEnabledFor(logging.DEBUG):
            log_message = f"First URL to be requested in this loop: {first_url}"
            log.debug(log_message)
            self.send_internal_collector_message(log_message, level="debug")

        # Counter initialization
        total_requests_counter: int = 0
        total_received_messages_counter: int = 0
        total_removed_messages_counter: int = 0
        total_generated_messages_counter: int = 0

        # This line only exists because the requests simulation
        request: MockRequest = MockRequest(persisted_info, max_number_of_messages_per_page)

        keep_reading: bool = True
        first_request: bool = True
        next_url = None
        while keep_reading:
            # Request execution
            if first_request:
                response: MockResponse = request.get(url=first_url, access_token=access_token)
                first_request = False

                # Clean messages using previously saved information
                messages = self._clean_message_list_using_persisted_data(response.content, persisted_info)
            else:
                response: MockResponse = request.get(url=next_url, access_token=access_token)
                messages = response.content

            total_requests_counter += 1
            total_received_messages_counter += len(response.content)
            total_removed_messages_counter += len(response.content) - len(messages)
            total_generated_messages_counter += len(messages)

            next_url = response.next_url
            if next_url is None:
                keep_reading = False

            if log.isEnabledFor(logging.DEBUG):
                log_message = \
                    f"Requested to \"{response.request_url}\", " \
                    f"received {len(response.content)} messages, " \
                    f"removed {len(response.content) - len(messages)} messages, " \
                    f"next page url: \"{response.next_url}\""
                log.debug(log_message)
                self.send_internal_collector_message(log_message, level="debug")

            # Send data to output
            self._send_data_info(messages, tag)

            if log.isEnabledFor(logging.DEBUG):
                log_message = f"Messages sent to output, used tag: \"{tag}\""
                log.debug(log_message)
                self.send_internal_collector_message(log_message, level="debug")

            persisted_data = self._persist_data_info(messages, response)

            if log.isEnabledFor(logging.DEBUG):
                log_message = f"Persisted data: {persisted_data}"
                log.debug(log_message)
                self.send_internal_collector_message(log_message, level="debug")

        return total_requests_counter, \
               total_received_messages_counter, \
               total_removed_messages_counter, \
               total_generated_messages_counter, \
               tag

    def _get_persisted_data_info(self) -> dict:
        """

        :return:
        """

        previous_state = self.persistence_object.load_state(no_log_traces=True)
        return previous_state

    def _prepare_tag(self):
        """

        :return:
        """

        base_tag = self.collector_variables["base_tag"]
        return base_tag.format(
            collector_version=CollectorExample11Puller.COLLECTOR_VERSION
        )

    def _create_first_url(self, retrieving_timestamp: datetime, persisted_info=None) -> str:
        """

        :param retrieving_timestamp:
        :param persisted_info:
        :return:
        """

        if persisted_info:
            last_timestamp = Utils.get_datetime_from_str(persisted_info["last_timestamp"])
        else:
            last_timestamp = retrieving_timestamp

        last_timestamp_str: str = Utils.get_str_from_datetime(last_timestamp)
        base_url: str = self.collector_variables["base_url"]
        region: str = self.collector_variables["region"]
        return base_url.format(since=last_timestamp_str, region=region)

    def _persist_data_info(self, messages: list, response: MockResponse) -> dict:
        """

        :param messages:
        :param response:
        :return:
        """

        if messages:
            state = self.persistence_object.load_state(no_log_traces=True)
            if state is None:
                state = {}

            last_timestamp = None
            id_list = []
            for message in messages[::-1]:
                message_timestamp = Utils.get_datetime_from_str(message["timestamp"])
                if last_timestamp is None:
                    last_timestamp = message_timestamp
                if last_timestamp == message_timestamp:
                    id_list.append(message["id"])
                else:
                    break

            state["last_timestamp"] = Utils.get_str_from_datetime(last_timestamp)
            state["id_list"] = id_list
            state["last_messages_with_same_timestamp"] = response.last_messages_with_same_timestamp
            self.persistence_object.save_state(state, no_log_traces=True)
            return state

    def _send_data_info(self, messages: list, tag: str):
        """

        :param messages:
        :param tag:
        :return:
        """

        for message in messages:
            self.send_standard_message(datetime.now(), tag, json.dumps(message))

    def _clean_message_list_using_persisted_data(self, messages, persisted_info):
        """

        :param messages:
        :param persisted_info:
        :return:
        """

        if persisted_info:
            already_sent_counter: int = 0
            already_sent_message_ids = persisted_info["id_list"]
            for message in messages:
                if message["id"] in already_sent_message_ids:
                    already_sent_counter += 1
                else:
                    break

            if log.isEnabledFor(logging.DEBUG):
                log_message = f"Removed already sent messages from received message list"
                log.debug(log_message)
                self.send_internal_collector_message(log_message, level="debug")

            return messages[already_sent_counter:]
        return messages

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass
