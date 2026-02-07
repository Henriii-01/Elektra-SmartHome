"""Base entity for the Elektra Verve integration."""

from __future__ import annotations

from homeassistant.const import CONF_HOST
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import ElektraVerveCoordinator


class ElektraVerveEntity(CoordinatorEntity[ElektraVerveCoordinator]):
    """Base class for all Elektra Verve entities."""

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
