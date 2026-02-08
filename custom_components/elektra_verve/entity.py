"""Base entities for the Elektra Verve integration."""

from __future__ import annotations

from asyncio import TimeoutError
from typing import Any

import aiohttp
from homeassistant.const import CONF_HOST
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import ElektraVerveCoordinator


class ElektraVerveEntity(CoordinatorEntity[ElektraVerveCoordinator]):
    """Common device info and helpers for Elektra Verve entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: ElektraVerveCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.serial_number)},
            name="Elektra Verve",
            manufacturer=MANUFACTURER,
            model=MODEL,
            serial_number=coordinator.serial_number,
            sw_version=coordinator.firmware_version,
            configuration_url=f"http://{coordinator.config_entry.data[CONF_HOST]}/",
        )

    async def _async_require_data(self) -> dict[str, Any]:
        """Ensure coordinator data is available, refreshing if needed."""

        if self.coordinator.data is None:
            await self.coordinator.async_refresh()
        if self.coordinator.data is None:
            raise HomeAssistantError("Device data unavailable for write")
        return self.coordinator.data

    async def _async_write_register(self, register: int, value: int) -> None:
        """Write to a device register with unified error handling."""

        try:
            success = await self.coordinator.client.async_write_register(register, value)
            if not success:
                raise HomeAssistantError(
                    f"Device did not acknowledge write to register {register}"
                )
        except (aiohttp.ClientError, TimeoutError) as err:
            raise HomeAssistantError(f"Failed to communicate with device: {err}") from err


class ElektraVerveDescribedEntity(ElektraVerveEntity):
    """Entity that derives its identity from an entity description."""

    def __init__(self, coordinator: ElektraVerveCoordinator, description: Any) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.serial_number}_{description.key}"
