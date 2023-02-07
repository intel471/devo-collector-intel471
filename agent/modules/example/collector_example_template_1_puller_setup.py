import logging

from devocollectorsdk.templates.template_1_puller_setup import Template1CollectorPullerSetup

log = logging.getLogger(__name__)


class TemplateExample1PullerSetup(Template1CollectorPullerSetup):

    def service_auth_is_defined(self) -> bool:
        return True

    def build_authentication(self) -> None:
        pass

    def service_auth_is_valid(self) -> bool:
        return True

    def refresh_auth(self) -> None:
        pass

    def remote_source_is_pullable(self) -> bool:
        return True
