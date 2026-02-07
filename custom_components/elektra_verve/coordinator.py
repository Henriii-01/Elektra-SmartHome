"""DataUpdateCoordinator for the Elektra Verve integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN
from .elektra_client import ElektraVerveClient

_LOGGER = logging.getLogger(__name__)


class ElektraVerveCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls the Elektra Verve device over HTTP."""

    config_entry: ConfigEntry
    client: ElektraVerveClient
    serial_number: str
    firmware_version: str

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        client: ElektraVerveClient,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=config_entry,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client

    async def _async_setup(self) -> None:
        """Fetch initial data and extract device identifiers.

        Called once during async_config_entry_first_refresh.
        """
        data = await self.client.async_get_status()
        self.serial_number = str(data.get("SERIAL_NUMBER", "unknown"))
        self.firmware_version = str(data.get("FW_REL", "unknown"))

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch latest status from the device."""
        try:
            return await self.client.async_get_status()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with device: {err}") from err
