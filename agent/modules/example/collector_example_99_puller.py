import logging
import secrets
import string
from datetime import datetime

from agent.modules.example.exceptions.exceptions import ExampleException
from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract
# noinspection PyUnresolvedReferences
from devocollectorsdk.message.message import Message

log = logging.getLogger(__name__)


def _generate_example_message(size_in_bytes: int) -> str:
    """
    This function generates one test message.
    :size_in_bytes: Number of bytes of the message to generate.
    """

    assertion_base = "PullerFunction::_generate_example_message() ->"

    assert isinstance(size_in_bytes, int), f"{assertion_base} size_in_bytes must be a int instance."
    assert size_in_bytes > 0, f"{assertion_base} size_in_bytes must more than 0."
    assert size_in_bytes <= 4096, f"{assertion_base} size_in_bytes must cannot be more than 4096 Bytes."

    alphabet: str = string.ascii_letters + string.digits
    msg: str = ''.join(secrets.choice(alphabet) for _ in range(size_in_bytes))

    return msg


def _generate_example_messages(number_of_messages: int, size_in_bytes: int) -> [str]:
    """
    This function generates the test messages.
    :number_of_messages: Number of messages to generate.
    :size_in_bytes: Number of bytes of the message to generate.
    """

    assertion_base = "PullerFunction::_generate_example_messages() ->"

    assert isinstance(number_of_messages, int), f"{assertion_base} size_in_bytes must be an int instance."
    assert number_of_messages > -1, f"{assertion_base} number_of_messages cannot be less than 0."
    assert number_of_messages <= 10000, f"{assertion_base} number_of_messages cannot be more than 10000."

    # We call only one time to the msg generator
    msg: str = _generate_example_message(size_in_bytes)

    message_list: [str] = [msg for _ in range(number_of_messages)]

    return message_list


class CollectorExample99Puller(CollectorPullerAbstract):
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
    #         self.output_queue
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

        log_message = f"{self.getName()} Starting the execution of init_variables()"
        log.debug(log_message)
        if log.isEnabledFor(logging.DEBUG):
            self.send_internal_collector_message(log_message, level="debug")

        # Initialization of properties from credentials section from configuration
        credentials_section = input_config.get("credentials")

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

            message_size_in_bytes: int = service_config.get("message_size_in_bytes")
            if message_size_in_bytes:
                self.collector_variables["message_size_in_bytes"] = message_size_in_bytes
            else:
                raise ExampleException(
                    7,
                    "Missing required \"message_size_in_bytes\" property "
                    "from \"module_properties\" section in collector definitions"
                )

            stop_after_in_seconds: int = service_config.get("stop_after_in_seconds")
            if stop_after_in_seconds:
                self.collector_variables["stop_after_in_seconds"] = stop_after_in_seconds
            else:
                raise ExampleException(
                    8,
                    "Missing required \"stop_after_in_seconds\" property "
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
        self.collector_variables["init_timestamp"] = datetime.utcnow()

        log_message = f"{self.getName()} Finalizing the execution of init_variables()"
        log.debug(log_message)
        if log.isEnabledFor(logging.DEBUG):
            self.send_internal_collector_message(log_message, level="debug")

    def pre_pull(self, retrieving_timestamp: datetime):
        base_tag = self.collector_variables["base_tag"]
        self.collector_variables["tag"] = base_tag.format(
            collector_version=CollectorExample99Puller.COLLECTOR_VERSION
        )

    def pull(self, retrieving_timestamp: datetime):
        log_message = "Starting pull()"
        log.debug(log_message)
        if log.isEnabledFor(logging.DEBUG):
            self.send_internal_collector_message(log_message, level="debug")

        # It is recommended to send some stats info to output

        start_time_overall = datetime.utcnow()

        requests_counter, received_messages_counter, removed_messages_counter, generated_messages_counter, tag_used = \
            self.__pull_execution(retrieving_timestamp)

        elapsed_time_overall = (datetime.utcnow() - start_time_overall).total_seconds()
        elapsed_time_per_message_overall = (elapsed_time_overall / received_messages_counter) * 1000 \
            if received_messages_counter > 0 else elapsed_time_overall

        log_message = \
            f"Number of requests {requests_counter}, received {received_messages_counter} message(s), " \
            f"removed {removed_messages_counter} message(s), " \
            f"generated and sent {generated_messages_counter} message(s), " \
            f"tag used: \"{tag_used}\". avg_time_per_source_message: {elapsed_time_per_message_overall:0.3f} ms"
        log.info(log_message)
        if log.isEnabledFor(logging.INFO):
            self.send_internal_collector_message(log_message, level="info")

        log_message = "Finalizing pull()"
        log.debug(log_message)
        if log.isEnabledFor(logging.DEBUG):
            self.send_internal_collector_message(log_message, level="debug")

    def __pull_execution(self, retrieving_timestamp: datetime) -> (int, int, int, int, str):

        max_number_of_messages_per_page: int = self.collector_variables["max_number_of_messages_per_page"]
        message_size_in_bytes: int = self.collector_variables["message_size_in_bytes"]

        init_timestamp: datetime = self.collector_variables["init_timestamp"]
        elapsed_seconds = (datetime.utcnow() - init_timestamp).total_seconds()
        if elapsed_seconds > self.collector_variables["stop_after_in_seconds"]:
            log.info(f"Stopping the collector")
            max_number_of_messages_per_page = 0
            self.running_flag = False

        tag: str = self.collector_variables["tag"]

        # Counter initialization
        total_requests_counter: int = 1
        total_received_messages_counter: int = max_number_of_messages_per_page
        total_removed_messages_counter: int = 0
        total_generated_messages_counter: int = max_number_of_messages_per_page

        start_time = datetime.utcnow()
        messages: [str] = _generate_example_messages(max_number_of_messages_per_page, message_size_in_bytes)
        elapsed_seconds_generating = (datetime.utcnow() - start_time).total_seconds()

        start_time = datetime.utcnow()
        self.send_standard_messages(datetime.utcnow(), tag, messages)
        elapsed_seconds_sending = (datetime.utcnow() - start_time).total_seconds()

        log.info(f"Elapsed time when generating/sending messages: "
                 f"{elapsed_seconds_generating:0.3f}/{elapsed_seconds_sending:0.3f} seconds")

        return (
            total_requests_counter,
            total_received_messages_counter,
            total_removed_messages_counter,
            total_generated_messages_counter,
            tag
        )

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass
