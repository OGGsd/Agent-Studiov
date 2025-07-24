from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import override

from axie_studio.services.factory import ServiceFactory
from axie_studio.services.telemetry.service import TelemetryService

if TYPE_CHECKING:
    from axie_studio.services.settings.service import SettingsService


class TelemetryServiceFactory(ServiceFactory):
    def __init__(self) -> None:
        super().__init__(TelemetryService)

    @override
    def create(self, settings_service: SettingsService):
        return TelemetryService(settings_service)
