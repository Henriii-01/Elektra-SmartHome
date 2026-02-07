"""Switch platform for the Elektra Verve integration."""

from __future__ import annotations

from typing import Any

import aiohttp

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ElektraVerveSwitchDescription, SWITCH_DESCRIPTIONS
from .coordinator import ElektraVerveCoordinator
from .entity import ElektraVerveEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Elektra Verve switches from a config entry."""
    coordinator: ElektraVerveCoordinator = entry.runtime_data
    async_add_entities(
        ElektraVerveSwitch(coordinator, description)
        for description in SWITCH_DESCRIPTIONS
    )


class ElektraVerveSwitch(ElektraVerveEntity, SwitchEntity):
    """Switch entity for the Elektra Verve."""

    entity_description: ElektraVerveSwitchDescription

    def __init__(
        self,
        coordinator: ElektraVerveCoordinator,
        description: ElektraVerveSwitchDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.serial_number}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._write(self.entity_description.on_fn)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._write(self.entity_description.off_fn)

    async def _write(self, value_fn) -> None:
        """Write a computed value to the device register."""
        try:
            value = value_fn(self.coordinator.data or {})
            success = await self.coordinator.client.async_write_register(
                self.entity_description.register, value
            )
            if not success:
                raise HomeAssistantError(
                    f"Device did not acknowledge write to register "
                    f"{self.entity_description.register}"
                )
        except (aiohttp.ClientError, TimeoutError) as err:
            raise HomeAssistantError(
                f"Failed to communicate with device: {err}"
            ) from err
        await self.coordinator.async_request_refresh()
