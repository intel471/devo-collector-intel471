import logging
from datetime import datetime

import time

# noinspection PyUnresolvedReferences
from agent.modules.example.collector_example_3_puller_setup import CollectorExample3PullerSetup
from agent.modules.example.exceptions.exceptions import ExampleException
from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract

log = logging.getLogger(__name__)

logging.getLogger("faker.factory").setLevel(logging.WARNING)


class CollectorExample3Puller(CollectorPullerAbstract):

    FORMAT_VERSION = 1

    # def create_setup_instance(
    #         self,
    #         setup_class_name: str,
    #         autosetup_enabled: bool,
    #         collector_variables: dict) -> CollectorPullerSetupAbstract:
    #     """
    #
    #     :param setup_class_name:
    #     :param autosetup_enabled:
    #     :param collector_variables:
    #     :return:
    #     """
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

        self.log_debug(f'{self.name} Starting the execution of init_variables()')

        # Initialization of properties from credentials section from configuration
        credentials_section = input_config.get("credentials")
        if credentials_section is None:
            raise ExampleException(
                3, "Missing required \"credentials\" section in the configuration"
            )

        username = credentials_section.get("username")
        if username is None:
            raise ExampleException(
                0, "Missing required \"username\" property from \"credentials\" section in configuration"
            )
        self.collector_variables["username"] = username

        password = credentials_section.get("password")
        if password is None:
            raise ExampleException(
                1, "Missing required \"password\" property from \"credentials\" section in configuration"
            )
        self.collector_variables["password"] = password

        # Initialization of properties from module_properties section from definitions file
        module_properties = module_definition.get("module_properties")
        if module_properties is None:
            raise ExampleException(
                7,
                "Missing required \"module_properties\" section in the collector definitions"
            )

        base_url: str = module_properties.get("base_url")
        if base_url is None:
            raise ExampleException(
                4,
                "Missing required \"base_url\" property from \"module_properties\" "
                "section in collector definitions"
            )
        self.collector_variables["base_url"] = base_url

        base_tag: str = module_properties.get("base_tag")
        if base_tag is None:
            raise ExampleException(
                5,
                "Missing required \"base_tag\" property from \"module_properties\" "
                "section in collector definitions"
            )
        self.collector_variables["base_tag"] = base_tag

        max_number_of_messages_per_page: int = module_properties.get("max_number_of_messages_per_page")
        if max_number_of_messages_per_page is None:
            raise ExampleException(
                6,
                "Missing required \"max_number_of_messages_per_page\" property "
                "from \"module_properties\" section in collector definitions"
            )
        self.collector_variables["max_number_of_messages_per_page"] = max_number_of_messages_per_page

        # Getting a property from the configuration (if exists)
        if "max_number_of_messages_per_page" in service_config:
            self.collector_variables["max_number_of_messages_per_page"]: int = \
                service_config["max_number_of_messages_per_page"]

        self.collector_variables["key1"] = "value1"

        self.log_debug(f'{self.name} Finalizing the execution of init_variables()')

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

        self.log_debug('Starting pull()')

        example_tag = "my.app.if_framework.example_3"
        example_content = "Example text from \"example_3\""

        self.send_standard_message(datetime.utcnow(), example_tag, example_content)
        time.sleep(1)
        self.send_standard_message(datetime.utcnow(), example_tag, example_content)

        self.log_debug('Messages sent to output')

        self.log_debug('Finalizing pull()')

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass
