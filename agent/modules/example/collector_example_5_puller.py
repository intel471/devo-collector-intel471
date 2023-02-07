import json
import logging
import time
from datetime import datetime
from typing import Any

from devocollectorsdk.commons.obfuscation_utils import ObfuscationUtils
from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract
from devocollectorsdk.inputs.collector_puller_setup_abstract import CollectorPullerSetupAbstract
# noinspection PyUnresolvedReferences
from agent.modules.example.collector_example_5_puller_setup import CollectorExample5PullerSetup

log = logging.getLogger(__name__)

logging.getLogger("faker.factory").setLevel(logging.WARNING)


class CollectorExample5Puller(CollectorPullerAbstract):

    FORMAT_VERSION = 1

    def create_setup_instance(
            self,
            setup_class_name: str,
            autosetup_enabled: bool,
            collector_variables: dict) -> CollectorPullerSetupAbstract:
        """

        :param setup_class_name:
        :param autosetup_enabled:
        :param collector_variables:
        :return:
        """

        setup_class = globals()[setup_class_name]
        return setup_class(
            self,
            collector_variables,
            autosetup_enabled,
            self.input_id,
            self.input_name,
            self.input_config,
            self.input_definition,
            self.service_name,
            self.service_type,
            self.service_config,
            self.service_definition,
            self.module_name,
            self.module_config,
            self.module_definition,
            self.persistence_object,
            self.output_queue,
            self.submodule_name,
            self.submodule_config
        )

    def init_variables(self,
                       input_config: dict,
                       input_definition: dict,
                       service_config: dict,
                       service_definition: dict,
                       module_config: dict,
                       module_definition: dict,
                       submodule_config: Any) -> None:
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

        example_tag = "my.app.if_framework.example_1"
        example_content = {
            "name": "Peter",
            "Surname": "Griffin",
            "id": 12345,
            "details": {
                "location": {
                    "address": "Main street",
                    "number": 123
                },
                "married": True,
                "id_card": "1234567890Z",
                "iban": "ES341234123412341234"
            }
        }
        # sanitize_keys = [
        #     ["id"],
        #     ["details", "location", "*"],
        #     ["details", "married"],
        #     ["details", "id_card"],
        #     ["details", "iban"],
        #
        # ]

        sensitive_data = [
            {
                "name": ["details", "iban"],
                "string_patterns": [
                    "[0-9a-zA-Z](?=.*.{4})"
                ]
            },
            {
                "name": ["id"],
                "value": -1

            },
            {
                "name": ["details", "married"],
                "value": False

            },
            {
                "name": ["details", "location", "*"]
            }
        ]

        sanitized_content = ObfuscationUtils.process_json(example_content, sensitive_data)
        self.send_standard_message(datetime.utcnow(), example_tag, sanitized_content)
        time.sleep(1)

        example_content_str = json.dumps(example_content)
        sanitized_content = ObfuscationUtils.process_json(example_content_str, sensitive_data)
        self.send_standard_message(datetime.utcnow(), example_tag, sanitized_content)

        self.log_debug("Messages sent to output")

        self.log_debug('Finalizing pull()')

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass
