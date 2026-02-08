"""Number platform for the Elektra Verve integration."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ElektraVerveNumberDescription, NUMBER_DESCRIPTIONS
from .coordinator import ElektraVerveCoordinator
from .entity import ElektraVerveDescribedEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Elektra Verve number entities from a config entry."""
    coordinator: ElektraVerveCoordinator = entry.runtime_data
    async_add_entities(
        ElektraVerveNumber(coordinator, description)
        for description in NUMBER_DESCRIPTIONS
    )


class ElektraVerveNumber(ElektraVerveDescribedEntity, NumberEntity):
    """Number entity for the Elektra Verve."""

    entity_description: ElektraVerveNumberDescription

    def __init__(
        self,
        coordinator: ElektraVerveCoordinator,
        description: ElektraVerveNumberDescription,
    ) -> None:
        super().__init__(coordinator, description)

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.coordinator.data is None:
            return None
        value = self.entity_description.value_fn(self.coordinator.data)
        return float(value) if value is not None else None

    @property
    def native_min_value(self) -> float | None:
        """Return dynamic min from device data, or static fallback."""
        if self.coordinator.data and self.entity_description.min_fn:
            val = self.entity_description.min_fn(self.coordinator.data)
            if val is not None:
                return float(val)
        return self.entity_description.native_min_value

    @property
    def native_max_value(self) -> float | None:
        """Return dynamic max from device data, or static fallback."""
        if self.coordinator.data and self.entity_description.max_fn:
            val = self.entity_description.max_fn(self.coordinator.data)
            if val is not None:
                return float(val)
        return self.entity_description.native_max_value

    async def async_set_native_value(self, value: float) -> None:
        """Write the new value to the device register."""
        data = await self._async_require_data()
        register_value = self.entity_description.command_fn(value, data)
        await self._async_write_register(self.entity_description.register, register_value)
        await self.coordinator.async_refresh()
