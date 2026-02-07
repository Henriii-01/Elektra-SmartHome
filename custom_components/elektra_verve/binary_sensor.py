"""Binary sensor platform for the Elektra Verve integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import BINARY_SENSOR_DESCRIPTIONS, ElektraVerveBinarySensorDescription
from .coordinator import ElektraVerveCoordinator
from .entity import ElektraVerveEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Elektra Verve binary sensors from a config entry."""
    coordinator: ElektraVerveCoordinator = entry.runtime_data
    async_add_entities(
        ElektraVerveBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class ElektraVerveBinarySensor(ElektraVerveEntity, BinarySensorEntity):
    """Binary sensor entity for the Elektra Verve."""

    entity_description: ElektraVerveBinarySensorDescription

    def __init__(
        self,
        coordinator: ElektraVerveCoordinator,
        description: ElektraVerveBinarySensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.serial_number}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
