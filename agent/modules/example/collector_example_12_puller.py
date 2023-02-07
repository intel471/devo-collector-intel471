import logging
from datetime import datetime

from agent.modules.example.exceptions.exceptions import ExampleException
from devocollectorsdk.inputs.collector_puller_abstract import CollectorPullerAbstract
# noinspection PyUnresolvedReferences
from devocollectorsdk.message.message import Message

log = logging.getLogger(__name__)

logging.getLogger("faker.factory").setLevel(logging.WARNING)


def _generate_example_message() -> str:
    # faker = Faker()
    # message_timestamp = Utils.get_str_from_datetime(datetime.now())
    return "{" \
           "\"id\": \"12345678\", " \
           "\"timestamp\": \"2020\", " \
           "\"name\": \"Devo\", " \
           "\"address\": \"150 Cambridge Park Dr #702, MA\"" \
           "}"


def _generate_example_messages(number_of_messages: int) -> list:
    # faker = Faker()
    message_list = []

    # message_timestamp = Utils.get_str_from_datetime(datetime.now())
    # {
    #     # "id": uuid.uuid4().hex,
    #     "id": "1",
    #     # "timestamp": message_timestamp,
    #     "timestamp": "2020",
    #     "name": "Devo",
    #     "address": "150 Cambridge Park Dr #702"
    #     # "name": faker.name(),
    #     # "address": faker.address()
    # }

    if number_of_messages > 0:
        message_content = \
            "A00000000000000000000000000000000000000000000ap8pVWiL4rbSo52edIbaHA32uYkERNqkglEAq8AZlGBiSkikfePK6cGaHfnelvIOP00DBXzaTl59JXoE0fX" \
            "zaxaGk4r5txt1iRY3gayrVk7QvhOQO8xfZjDNcn64LhX9lPbmvUjuvyDenB2lHKUosG8Hr9nutUrX2LCKcbsz4CN8zhEjv7J3yRta6nmuTa4Hqcoz82rhbkXct49OH17" \
            "tD3zUZlbe1ayr1BzL3ZQmDYy5vFigvvUv690w4EyqlwmBXv3UNva2JHUUUSqsOJtqfQe9SgVAH16vzZ8xUIBEdqDLAH6UWGJwwSi5wwU25RO7aQ4xan7IGJijLJfglJh" \
            "uo6XQaVZ1G59jqhypaqC04YkyoMCdKpLwyr7cRYTbDbgSfchXtuIJqKcZ30vOGP2PBO0nr16EJRlNVd6wr23Ogcc1cxKVIxQ3ZGh7dJFjfjQjnekeSU6lp9XtFeRJrDY" \
            "X55KDT1bIHx845a16xcA0kN0N1HJeBkpJF7U4JelyBmzml1mXFTyHTDbAaBCVc5dYzWgaIwFmy4NJg9xiwspyaxcI69eJ5GaoUaVC0TpZQGeigBfHsF7gni5hBiCxqHA" \
            "7xYMBi2T1RddR2SkUavpXfpzvi3z3jhu8jukc1V9C3xYkOgYRfyoULQUbHs3XC7Fghvu1ByWYiDOrnnvDRSUlIwTiI7ocdG2slHCONMh3bMJ6FT4tUVdGGosgJP6O3bq" \
            "oFO4VLPe1XrVTrTVB4xDlBcPoqmSvMS8akgbkcr54vwhXWPQAwCaNF9hoC0S8US7UiP1j5cyQRVtcSMkWZwgYZA0Bj1f2s2tSZOpuv08wHXBlfeQghVXG0l7zs5ZgzTq" \
            "yEfcexDLTRRGYcqciaeOFyJ9951omp2U5wqVnkShfwoeoIh9cOd7NNl5jdeAolN5VXP8z6gk4ccdpXXcfJZKbiIIbcJoLhpotuhu2gH7NNcKtkzsOTSLFB8AnIo24f5Z" \
            "vcyy2ilMYCwdV8tyq0MyzPZBim9LEnTxzTU7Q4LtxhaLUbJ4uhSoPU48ZV35vROMzB33r6SfKDFyv8WSFvMWqQ8znQLut6zzzIJ83wIP2O4VkDpIwNsYUgzzhqNPCrwQ" \
            "VqqT8NWxgckWytmjtVVxc5RTwlzBQ8etCF8tF7d8ZbfxHe7xPKFQIrEgsbSz0Of8gzsUUtMHzfmg3a7u82MZ20T0Xo1DNqw99dib6Xk0ySvDIkyG5phYjjXCqbwHQ4Wn" \
            "lW3VrJEk7CoqyLrWho8y0J4CWPNvwn2jiR0218JSQUrEETyLBOcbB1rb90v8dRQpx9zpUjfKeCIBqBhKAm5Y7wQbD4jZb1oTlL6M8mS9HRnRNf2qx4TLPlGWg8KO37by" \
            "yUeP7vfL2jufC1XH6cPfgeWlZbeSsB6CCW4b4iR1MSIPQAhZf6tOvYyDQX4g9qifPtOrw9KSFNDLKcUejIALhaPQHSkg7VQ5T8dWMa5A2dXiBpJFPM3y0QETdQBdP4fg" \
            "sY2tKv8OVmfXIGRdWy9Je7y1B27okuv3gJICICp8y5DWd9WhV6y8DSpYjBeL6MtfO7UXVbHVwWBbREcRIucMw3JpMckHQtCFaHjRXkjW2xHq66H4CH2LC9SVacjQIixZ" \
            "JXzMEfHyPp6dQVVsvWVRTpMoalDabkTTwM9mmTau7iQlEYJpx7yix0cCuiINYk8nxuHW7n0aZ34ATqQ9vEFSSHe7KTEL3DmHswnpFXBnD9ZSO9QQpvmtqielwqxMno3d" \
            "cAxIOE24I4umzlIFKimTvvSXkQ4pRNFyDN0XYLPAUJCgqUoztYm6O7Mh9Aa4x2ggh27sviWmSd1hmUk5ccJrm24Cp2lEusunWMq1ruSKZhUveV0Eqq6rx1uwRoZnOnVD" \
            "eLlz3lk0UkiD4JGufzpBmvWAzsggVFzPnUE6akYh1v3VoY8PW9ahctqkOs6Yf9QGX8ysOBwIeNDrhvYWnkWLQexvJKFEYZgnWKqiCamXPkAMtXHUCVwedNf4YluSqvD9" \
            "Y20VWUMAQj5hWI4Unge19C6CdxchjOopVmKMy98ZrpFMGwDxzRsJs3vJCF7qw9OdvogllNWDrlwjigOUJVFVRZOxQLkRAeo3GezVKn7LBaafgCGc9ORrOiAUV2BJ88z3" \
            "H5WkWGxGmvsvyEOiwWXr0a9RPSlkVFAud0Qus7VTh35R6hq8O51PBZz7LZ8808OZGkBxqn77n26K1fsgifptQbNe4IvlnBXcN6CrhNmAYqqTZJqV8W1pEXjZ5xkA78w6" \
            "fOD9kv1vW9tWHz36qkDi2p1I1zw1lKgl1gl4x1eGuZpUyanBTeDNMkn8ESHWToAPB8Ia4PPMgZzFueKnQG3niAcIviG7ILnUWSJqyHIVvzh65eycnnwQ3rl1wIWCv8PZ" \
            "BTTsjpd6rOgxwtytHCxOl0atViGLVkchJmWtqCVgHVRZkc0a5UxX94EeCiBQtaEKDJW08F0AHXyhLcPWTYeukdNTG5vAQdcb9iZtAKrTx7PpEubM4O0bmxK8r7fietEV" \
            "j0r9iiZheNbdeHtXVe2ELV2U65Q3uch9jstp6T86oJYTXRInoVApWDjjCsDu3hlH79uDThXF0krJsWehESTCdLDAR7SqQqCEI7Y0YiJxC64C0hqztRGn4MQwCwrKhXCh" \
            "xOSpk3QOPoxDd7AB3j2Pe2EmwcAO85I02rGPjoFAqi4KH47Sub1cL6AI9PPzFzlaWNFdiwXIm3ZEIrtQjyIZAYlvRPDWcX1VvDe3GZyXzvmNlbAEnwCLVEgTzaDfO4lW" \
            "j9d0NqEZ2OVQLq5muZiUdM0TqFiujlmk7C886iOO7oIU5RTugQPRDe2YSWiqTaw1ndj1usFhSpzDhcLh7lB3T7jO7uj6GHGHHjGx35Cm0OTDvM6sqa7dAUVC1E87287z" \
            "4XLfr6bAkWpSsY3otp74ZnB2xLkWx10Yu12S9lqBZAn8L1LAHtykA5ZSZ8VWMzXfsTsY8QvDVbCvVI4Udy7km0DvFeRtiCm2YgpLuqghwCdQV0bb9z8LFG73HKZlCRMY" \
            "5k6yLDxjh1XfxWG9tA47dCs3Gda0J2BN3z7AHZflpYgHSqu9SbrzA4XHPxo61mbwh2A0JofsFLxm22vYpiR27hvCdgo1oQsDEzXyGGnPCoB3ywCemB9dabMYAfRHEwKs" \
            "BNUwlnqnL7mKOEYFCaCjKcX7FZsjYjDdZb9DIXb7lobQj9Vws7dK2iyiqELx7YXHEZTUNNhsRM7Yk9X6sgMKgTSNfixjLWkajqOwAycvgcgxt5MJAT0LstWdWTlAoWeM" \
            "vdYuMemgN2rw4oFpV9tT84nLDka4LHUEOVffEx4rraDrEuVIwQcrxI0cI1H23QeNJ1MDwaYABbniUcqJq6zQ6KvcWiZ7lEpOLvsKCJCBrIGgqselMVjCa7U7Nxugrrb9" \
            "TE2TAIorW6OnCuwRwIBEGkUrEm0PbTUtcGXTdgCLFWCzZEMlJXiq4fJ3Vx1UYMqpKkxKogZ8uqrqF0gPZ6F9n5oJ8468QxYcLISoNx3x9Y3BiesLVhV5LDRRvAaSIVrU" \
            "jjPClBoaLtijDStfNYu5ncCx78eTP5od8zFc8B7m3e1Ekm0guXGJ6EujnVONRxVo14lrUvHbWTJSAlc5VMp3BX73Oce1F15D0QY6NoIcF3ZotGTam1ohSF3Z7FZLJrUw" \
            "fEOw5JZRlmNJfbkZdEjiFGjB0dem0x0wSZwM5BlglYtP9C3cHKrINha4FtjmlFGOpgF6cZaqgZeWaRdOcoeIbXyO9I0EAHqcBZycaUryPdstPoMrV7YRRTCLt8mLJQ5q" \
            "xMokdPZxjWqCVWRz8n3p1VqZV1wNyYPA6Cs7pGV441vSfJajzNzOS46nEHvPoJrZjnWPtZ2KUwsmz3GIkWcJK71HT8MJatQMn6CYoafH4DV7GmmwNu30uDzBApAayBpK" \
            "gJwqoKbbZOdOaAVurR4mXJmHBfXoOwDeQJLiGtLEg6xLQ954jZYA1rWWG4ZyhxjYQB7athHKHzHEEytznRIPy1uan1dL99999999999999999999999999999999999Z"

        # message_content = \
        #     "A00000000000000000000000000000000000000000000ap8pVWiL4rbSo52edIbaHA32uYkERNqkglEAq8AZlGBiSkikfePK6cGaHfnelvIOP00DBXzaTl59JXoE0fX" \
        #     "zaxaGk4r5txt1iRY3gayrVk7QvhOQO8xfZjDNcn64LhX9lPbmvUjuvyDenB2lHKUosG8Hr9nutUrX2LCKcbsz4CN8zhEjv7J3yRta6nmuTa4Hqcoz82rhbkXct49OH17" \
        #     "tD3zUZlbe1ayr1BzL3ZQmDYy5vFigvvUv690w4EyqlwmBXv3UNva2JHUUUSqsOJtqfQe9SgVAH16vzZ8xUIBEdqDLAH6UWGJwwSi5wwU25RO7aQ4xan7IGJijLJfglJh" \
        #     "uo6XQaVZ1G59jqhypaqC04YkyoMCdKpLwyr7cRYTbDbgSfchXtuIJqKcZ30vOGP2PBO0nr16EJRlNVd6wr23Ogcc1cxKVIxQ3ZGh7dJFjfjQjnekeSU6lp9XtFeRJrDY"

        # log.info(f"Generated message size: {len(message_content)} bytes")
        for _ in range(number_of_messages):
            # message_list.append(f'{{"a": "b", "n": {i:06d}}}')
            message_list.append(message_content)

            # message_list.append(
            #     "{"
            #     "\"id\": \"12345678\", "
            #     "\"timestamp\": \"2020\", "
            #     "\"name\": \"Peter Lowenbrau McFinnigan Griffin\", "
            #     "\"City\": \"Quahog\", "
            #     "\"Description\": \"Peter is a stereotypical blue-collar worker who frequently gets drunk with "
            #     "his neighbors and friends Cleveland Brown, Joe Swanson and Glenn Quagmire at 'The Drunken Clam,' Quahog's "
            #     "local tavern. In the season 4 episode 'Petarded', Peter discovered his low intellect falls slightly "
            #     "below the level for mental retardation after taking an I.Q. test, which places his I.Q. at around 70. "
            #     "Peter is known for his brash impulsiveness, which has led to several awkward situations, such as "
            #     "attempting to molest Meg in order to adopt a redneck lifestyle. He is easily influenced by anyone "
            #     "he finds interesting and will often try to replicate their lifestyle and behavior merely out of curiosity. "
            #     "He is incredibly jealous of other attractions Lois has in her life, an attitude which has led to extreme "
            #     "situations, such as when he assaulted a whale that kissed Lois at SeaWorld. In the third season episode 'Stuck T\""
            #     "}"
            # )
    return message_list


class CollectorExample12Puller(CollectorPullerAbstract):
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
    #         self.internal_queue
    #     )

    def init_variables(
            self,
            input_config: dict,
            input_definition: dict,
            service_config: dict,
            service_definition: dict,
            module_config: dict,
            module_definition: dict,
            submodule_config: dict) -> None:
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

        self.log_debug(f"{self.name} Starting the execution of init_variables()")

        # Initialization of properties from credentials section from configuration
        credentials_section = input_config.get("credentials")
        if not credentials_section:
            raise ExampleException(
                1,
                'Missing required "credentials" section in the configuration'
            )

        username = credentials_section.get("username")
        if not username:
            raise ExampleException(
                2,
                'Missing required "username" property from "credentials" section in configuration'
            )
        self.collector_variables["username"] = username

        password = credentials_section.get("password")
        if not password:
            raise ExampleException(
                3,
                'Missing required "password" property from "credentials" section in configuration'
            )
        self.collector_variables["password"] = password

        # Initialization of properties from module_properties section from definitions file
        module_properties = module_definition.get("module_properties")
        if not module_properties:
            raise ExampleException(
                4,
                'Missing required "module_properties" section in the collector definitions'
            )

        base_url: str = module_properties.get("base_url")
        if not base_url:
            raise ExampleException(
                5,
                'Missing required "base_url" property from "module_properties" '
                'section in collector definitions'
            )
        self.collector_variables["base_url"] = base_url

        base_tag: str = module_properties.get("base_tag")
        if not base_tag:
            raise ExampleException(
                6,
                'Missing required "base_tag" property from "module_properties" '
                'section in collector definitions'
            )
        self.collector_variables["base_tag"] = base_tag

        max_number_of_messages_per_page: int = module_properties.get("max_number_of_messages_per_page")
        if not max_number_of_messages_per_page:
            raise ExampleException(
                7,
                'Missing required "max_number_of_messages_per_page" property '
                'from "module_properties" section in collector definitions'
            )
        self.collector_variables["max_number_of_messages_per_page"] = max_number_of_messages_per_page

        # Getting a property from the configuration (if exists)
        if "max_number_of_messages_per_page" in service_config:
            self.collector_variables["max_number_of_messages_per_page"]: int = \
                service_config["max_number_of_messages_per_page"]

        self.collector_variables["region"] = submodule_config
        self.collector_variables["init_timestamp"] = datetime.utcnow()

        self.log_debug(f'{self.name} Finalizing the execution of init_variables()')

    def pre_pull(self, retrieving_timestamp: datetime) -> None:
        """

        :param retrieving_timestamp:
        :return:
        """
        base_tag = self.collector_variables["base_tag"]
        self.collector_variables["tag"] = base_tag.format(
            collector_version=CollectorExample12Puller.COLLECTOR_VERSION
        )

    def pull(self, retrieving_timestamp: datetime):
        # It is recommended to send some stats info to output

        start_time_overall = datetime.utcnow()

        requests_counter, \
        received_messages_counter, \
        removed_messages_counter, \
        generated_messages_counter, \
        tag_used, \
        elapsed_seconds_init, \
        elapsed_seconds_generating, \
        elapsed_seconds_sending = \
            self._get_data_and_send_to_devo(retrieving_timestamp)

        elapsed_time_overall = (datetime.utcnow() - start_time_overall).total_seconds()
        # elapsed_time_per_message_overall = (elapsed_time_overall / received_messages_counter) * 1000 \
        #     if received_messages_counter > 0 else elapsed_time_overall

        # log_message = \
        #     f"Number of requests {requests_counter}, received {received_messages_counter} message(s), " \
        #     f"removed {removed_messages_counter} message(s), generated and sent {generated_messages_counter} message(s), " \
        #     f"tag used: \"{tag_used}\". elapsed_time_overall: {elapsed_time_overall:0.3f}, " \
        #     f"avg_time_per_source_message: {elapsed_time_per_message_overall:0.3f} ms"
        log_message = \
            f"Number of messages: {received_messages_counter}, " \
            f"elapsed time in seconds (init/generating/adding/total): " \
            f"{elapsed_seconds_init}/" \
            f"{elapsed_seconds_generating}/" \
            f"{elapsed_seconds_sending}/" \
            f"{elapsed_time_overall}"
        log.debug(log_message)
        # if log.isEnabledFor(logging.INFO):
        #     self.send_internal_collector_message(log_message, level="info")

    def _get_data_and_send_to_devo(self, retrieving_timestamp: datetime) -> (int, int, int, int, str):

        start_time = datetime.utcnow()
        max_number_of_messages_per_page: int = self.collector_variables["max_number_of_messages_per_page"]
        init_timestamp: datetime = self.collector_variables["init_timestamp"]
        elapsed_seconds = (datetime.utcnow() - init_timestamp).total_seconds()
        if elapsed_seconds > 1800:
            log.info(f"Stopping the collector")
            max_number_of_messages_per_page = 0
            self.running_flag = False
        # elif elapsed_seconds > 600:
        #     max_number_of_messages_per_page = 0
        # elif elapsed_seconds > 480:
        #     max_number_of_messages_per_page = 1
        # elif elapsed_seconds > 360:
        #     max_number_of_messages_per_page = round(max_number_of_messages_per_page / 8)
        # elif elapsed_seconds > 240:
        #     max_number_of_messages_per_page = round(max_number_of_messages_per_page / 4)
        # elif elapsed_seconds > 120:
        #     max_number_of_messages_per_page = round(max_number_of_messages_per_page / 2)

        tag: str = self.collector_variables["tag"]

        # Counter initialization
        total_requests_counter: int = 1
        total_received_messages_counter: int = max_number_of_messages_per_page
        total_removed_messages_counter: int = 0
        total_generated_messages_counter: int = max_number_of_messages_per_page
        elapsed_seconds_init = (datetime.utcnow() - start_time).total_seconds()

        start_time = datetime.utcnow()
        messages = _generate_example_messages(max_number_of_messages_per_page)
        elapsed_seconds_generating = (datetime.utcnow() - start_time).total_seconds()

        start_time = datetime.utcnow()
        self._send_data_info(messages, tag, batch=True)
        elapsed_seconds_sending = (datetime.utcnow() - start_time).total_seconds()
        # log.info(
        #     f"Elapsed time in seconds (init/generating/adding): "
        #     f"{elapsed_seconds_init}/"
        #     f"{elapsed_seconds_generating}/"
        #     f"{elapsed_seconds_sending} seconds"
        # )

        return \
            total_requests_counter, \
            total_received_messages_counter, \
            total_removed_messages_counter, \
            total_generated_messages_counter, \
            tag, \
            elapsed_seconds_init, \
            elapsed_seconds_generating, \
            elapsed_seconds_sending

    def _send_data_info(self, messages: list, tag: str, batch: bool = False):
        if batch:
            message_batch = []
            for message in messages:
                message_batch.append(message)
            self.send_standard_messages(datetime.utcnow(), tag, message_batch)
        else:
            for message in messages:
                self.send_standard_message(datetime.utcnow(), tag, message)

    def module_finalization(self) -> None:
        """

        :return:
        """
        pass

    def pull_stop(self) -> None:
        """Not required for this puller"""
        pass

    def pull_pause(self, wait: bool = None) -> None:
        """Not required for this puller

        :param wait:
        """
        pass
