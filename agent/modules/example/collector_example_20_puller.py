import logging
from datetime import datetime

from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract

log = logging.getLogger(__name__)


class CollectorExample20Puller(CollectorPullerAbstract):

    # def create_setup_instance(
    #         self,
    #         setup_class_name: str,
    #         autosetup_enabled: bool,
    #         collector_variables: dict) -> CollectorPullerSetupAbstract:
    #     pass

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

        module_properties = module_definition.get("module_properties")
        if module_properties:

            base_url: str = module_properties.get("base_url")
            if base_url:
                self.collector_variables["base_url"]: str = base_url
            else:
                raise Exception(
                    "\"base_url\" property in module definition is not valid or empty."
                )
            base_tag: str = module_properties.get("base_tag")
            if base_tag:
                self.collector_variables["base_tag"]: str = base_tag
            else:
                raise Exception(
                    "\"base_tag\" property in module definition is not valid or empty."
                )

    def pre_pull(self, retrieving_timestamp: datetime):
        """Not required for this collector"""
        pass

    def pull(self, retrieving_timestamp: datetime):
        """

        :param retrieving_timestamp:
        :return:
        """

        base_url = self.collector_variables["base_url"]
        url = base_url.format(
            service_type=self.service_type
        )
        log.info(f"URL used: \"{url}\"")

        base_tag = self.collector_variables["base_tag"]
        messages = [
            '{"content": "message1"}',
            '{"content": "message2"}',
            '{"content": "message3"}'
        ]
        for message in messages:
            self.send_standard_message(datetime.utcnow(), base_tag, message)
        log.info("Pulling has been executed")

        self.send_standard_message("date", "my.app.simple_message.test1", "test_message")

        log.info("Here a pulling is executed")

    def pull_stop(self) -> None:
        """Not required for this collector"""
        pass

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this collector"""
        pass
