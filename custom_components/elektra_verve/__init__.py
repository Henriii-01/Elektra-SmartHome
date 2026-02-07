"""The Elektra Verve integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant

from .coordinator import ElektraVerveCoordinator
from .elektra_client import ElektraVerveClient

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SWITCH,
]

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry[ElektraVerveCoordinator]
) -> bool:
    """Set up Elektra Verve from a config entry."""
    client = ElektraVerveClient(hass, entry.data[CONF_HOST])
    coordinator = ElektraVerveCoordinator(hass, entry, client)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ConfigEntry[ElektraVerveCoordinator]
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
