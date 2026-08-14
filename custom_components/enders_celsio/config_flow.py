"""Config flow for Enders Celsio integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.const import CONF_ADDRESS
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DEVICE_TYPE,
    DEVICE_TYPE_BASE_STATION,
    DEVICE_TYPE_PROBE,
    DOMAIN,
    NAME_BASE_PREFIX,
    NAME_PROBE_PREFIX,
)
from .parser import parse_service_info

_LOGGER = logging.getLogger(__name__)


class EndersCelsioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Enders Celsio."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, str] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        self._discovery_info = discovery_info
        parsed_data = parse_service_info(discovery_info)

        device_name = discovery_info.name or "Enders Celsio"
        if parsed_data and parsed_data.name:
            device_name = parsed_data.name

        self.context["title_placeholders"] = {
            "name": device_name,
            "address": discovery_info.address,
        }

        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        assert self._discovery_info is not None

        if user_input is not None:
            device_name = self._discovery_info.name or "Enders Celsio"
            device_type = (
                DEVICE_TYPE_BASE_STATION
                if device_name.startswith(NAME_BASE_PREFIX)
                else DEVICE_TYPE_PROBE
            )
            return self.async_create_entry(
                title=f"{device_name} ({self._discovery_info.address})",
                data={
                    CONF_ADDRESS: self._discovery_info.address,
                    CONF_DEVICE_TYPE: device_type,
                },
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders={
                "name": self._discovery_info.name or "Enders Celsio",
                "address": self._discovery_info.address,
            },
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user manual step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()

            device_type = user_input.get(CONF_DEVICE_TYPE, DEVICE_TYPE_PROBE)
            return self.async_create_entry(
                title=f"Enders Celsio ({address})",
                data={
                    CONF_ADDRESS: address,
                    CONF_DEVICE_TYPE: device_type,
                },
            )

        # Scan for nearby Enders devices
        current_addresses = self._async_current_ids()
        for discovery_info in async_discovered_service_info(self.hass):
            address = discovery_info.address
            if address in current_addresses or address in self._discovered_devices:
                continue

            name = discovery_info.name or ""
            if name.startswith((NAME_PROBE_PREFIX, NAME_BASE_PREFIX)):
                self._discovered_devices[address] = f"{name} ({address})"

        if self._discovered_devices:
            schema = vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): vol.In(self._discovered_devices),
                }
            )
        else:
            schema = vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): str,
                    vol.Optional(CONF_DEVICE_TYPE, default=DEVICE_TYPE_PROBE): vol.In(
                        [DEVICE_TYPE_PROBE, DEVICE_TYPE_BASE_STATION]
                    ),
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
