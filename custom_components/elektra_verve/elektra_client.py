"""Async HTTP client for the Elektra Verve espresso machine."""

from __future__ import annotations

from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class ElektraVerveClient:
    """Async HTTP client for the Elektra Verve device.

    Protocol (reverse-engineered from device app.js):
      Read:  GET /elektra.txt            -> JSON with 20 fields
      Write: GET /web.cgi?elektra_write=<register>|<value>
    """

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        self._session = async_get_clientsession(hass, verify_ssl=False)
        self._base_url = f"http://{host}"
        self._timeout = aiohttp.ClientTimeout(total=5)

    async def async_get_status(self) -> dict[str, Any]:
        """Fetch /elektra.txt and return parsed JSON."""
        async with self._session.get(
            f"{self._base_url}/elektra.txt",
            timeout=self._timeout,
        ) as resp:
            resp.raise_for_status()
            return await resp.json(content_type=None)

    async def async_write_register(self, register: int, value: int) -> bool:
        """Write a register value via /web.cgi?elektra_write=register|value."""
        async with self._session.get(
            f"{self._base_url}/web.cgi",
            params={"elektra_write": f"{register}|{value}"},
            timeout=self._timeout,
        ) as resp:
            resp.raise_for_status()
            text = await resp.text()
        return "ELEKTRA" in text

    async def async_validate_connection(self) -> dict[str, Any]:
        """Validate connectivity and return initial device data.

        Used by config_flow to test the connection before creating an entry.
        Raises aiohttp.ClientError or TimeoutError on failure.
        """
        return await self.async_get_status()
