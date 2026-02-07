"""Sensor platform for the Elektra Verve integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ElektraVerveSensorDescription, SENSOR_DESCRIPTIONS
from .coordinator import ElektraVerveCoordinator
from .entity import ElektraVerveEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Elektra Verve sensors from a config entry."""
    coordinator: ElektraVerveCoordinator = entry.runtime_data
    async_add_entities(
        ElektraVerveSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class ElektraVerveSensor(ElektraVerveEntity, SensorEntity):
    """Sensor entity for the Elektra Verve."""

    entity_description: ElektraVerveSensorDescription

    def __init__(
        self,
        coordinator: ElektraVerveCoordinator,
        description: ElektraVerveSensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.serial_number}_{description.key}"

    @property
    def native_value(self):
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
