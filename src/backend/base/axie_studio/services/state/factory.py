from typing_extensions import override

from axie_studio.services.factory import ServiceFactory
from axie_studio.services.settings.service import SettingsService
from axie_studio.services.state.service import InMemoryStateService


class StateServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(InMemoryStateService)

    @override
    def create(self, settings_service: SettingsService):
        return InMemoryStateService(
            settings_service,
        )
