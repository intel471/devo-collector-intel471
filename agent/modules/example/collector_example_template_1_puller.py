from datetime import datetime

from devocollectorsdk.templates.template_1_puller import Template1CollectorPuller


class TemplateExamplePuller1(Template1CollectorPuller):

    def run_custom_init_variables_validations(self) -> None:
        self.collector_variables['up_to_date'] = False

    def prepull_default_state(self, retrieving_ts: datetime) -> dict:
        return {'retrieving_ts': retrieving_ts.isoformat()}

    def prepull_persistence_upgrade_steps(self, **kwargs) -> dict:
        pass

    def prepull_persistence_corrections_steps(self, **kwargs) -> dict:
        pass

    def prepull_persistence_reset_steps(self, **kwargs) -> dict:
        pass

    def execute_pull_logic(self, statistics: dict) -> None:
        calls = 0
        msgs = []
        msg = {
            'name': 'A name',
            'last_name': 'A Last name',
            'civil_state': {
                'married': True,
                'sons': [
                    {
                        'name': 'Son1 name',
                        'last_name': 'Son1 last name'
                    },
                    {
                        'key1': 'Son2 name',
                        'key2': 'Son2 last name'
                    }
                ]
            },
            'address': {
                'street': 'A very beautiful street',
                'number': 123
            }
        }
        msgs.append(msg)
        msgs.append(msg)

        for _ in range(10_000):
            with self.rate_limiter:
                # calls += 1
                # print('template puller', calls)
                self.send_standard_message(datetime.utcnow(), 'test.drop', msg)

        for _ in range(10_000):
            with self.rate_limiter:
                # calls += 1
                # print('template puller', calls)
                self.send_standard_messages(datetime.utcnow(), 'test.drop', msgs)

        self.collector_variables['up_to_date'] = True

    def is_data_up_to_date(self) -> bool:
        return self.collector_variables['up_to_date']

    def pull_stop(self) -> None:
        pass

    def pull_pause(self, wait: bool = None) -> None:
        pass
