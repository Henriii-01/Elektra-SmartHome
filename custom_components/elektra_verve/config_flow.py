"""Config flow for the Elektra Verve integration."""

from __future__ import annotations

import logging
import re
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_SSID

from .const import DEFAULT_HOST, DOMAIN
from .elektra_client import ElektraVerveClient

_LOGGER = logging.getLogger(__name__)


SSID_PATTERN = re.compile(r"^elektra-(?P<serial>[A-Za-z0-9]+)$", re.IGNORECASE)

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required(CONF_SSID): str})


class ElektraVerveConfigFlow(ConfigFlow, domain=DOMAIN):  # type: ignore[misc]
    """Handle a config flow for Elektra Verve."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            ssid = user_input[CONF_SSID].strip()
            match = SSID_PATTERN.match(ssid)

            if not match:
                errors[CONF_SSID] = "invalid_ssid"
            else:
                serial_from_ssid = match.group("serial")
                host = DEFAULT_HOST
                client = ElektraVerveClient(self.hass, host)

                try:
                    data = await client.async_validate_connection()
                except (aiohttp.ClientError, TimeoutError):
                    errors["base"] = "cannot_connect"
                except Exception:  # pragma: no cover - defensive
                    _LOGGER.exception("Unexpected error during config flow")
                    errors["base"] = "unknown"
                else:
                    device_serial = str(data.get("SERIAL_NUMBER", "")).strip()

                    if not device_serial:
                        errors["base"] = "unknown"
                    elif device_serial.lower() != serial_from_ssid.lower():
                        errors["base"] = "ssid_mismatch"
                    else:
                        await self.async_set_unique_id(device_serial)
                        self._abort_if_unique_id_configured(
                            updates={
                                CONF_HOST: host,
                                CONF_SSID: ssid,
                                "serial_number": device_serial,
                            }
                        )

                        return self.async_create_entry(
                            title=f"Elektra Verve ({device_serial})",
                            data={
                                CONF_HOST: host,
                                CONF_SSID: ssid,
                                "serial_number": device_serial,
                            },
                        )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
