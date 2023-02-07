import logging
from datetime import datetime
from typing import Any

import time

# noinspection PyUnresolvedReferences
from agent.modules.example.collector_failure_2_puller_setup import CollectorFailure2PullerSetup
from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract

log = logging.getLogger(__name__)

logging.getLogger("faker.factory").setLevel(logging.WARNING)


class CollectorFailure2Puller(CollectorPullerAbstract):

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

        log_message = f"{self.getName()} Starting the execution of init_variables()"
        log.debug(log_message)

        log_message = f"{self.getName()} Finalizing the execution of init_variables()"
        log.debug(log_message)

    def pre_pull(self, retrieving_timestamp: datetime):
        """Not required for this collector

        :param retrieving_timestamp:
        :return:
        """
        log_message = f"{self.getName()} Starting the execution of pre_pull()"
        log.debug(log_message)

        log_message = f"{self.getName()} Finalizing the execution of pre_pull()"
        log.debug(log_message)

    def pull(self, retrieving_timestamp: datetime):
        """

        :param retrieving_timestamp:
        :return:
        """

        log_message = "Starting pull()"
        log.debug(log_message)

        example_tag = "my.app.if_framework.example_1"
        example_content = "Example text from \"example_1\""

        self.send_standard_message(datetime.utcnow(), example_tag, example_content)
        time.sleep(1)
        self.send_standard_message(datetime.utcnow(), example_tag, example_content)

        log_message = "Messages sent to output"
        log.debug(log_message)

        log_message = "Finalizing pull()"
        log.debug(log_message)

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass
