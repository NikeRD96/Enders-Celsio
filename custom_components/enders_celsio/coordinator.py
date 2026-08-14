"""Coordinator for Enders Celsio BLE devices."""
from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

from homeassistant.components import bluetooth
from homeassistant.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
    async_last_service_info,
    async_register_callback,
)
from homeassistant.components.bluetooth.match import BluetoothCallbackMatcher
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import CONNECTION_BLUETOOTH, DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DEVICE_TYPE_BASE_STATION,
    DEVICE_TYPE_PROBE,
    DOMAIN,
)
from .parser import EndersCelsioData, parse_service_info

_LOGGER = logging.getLogger(__name__)


class EndersCelsioCoordinator(DataUpdateCoordinator[EndersCelsioData]):
    """Coordinator for Enders Celsio Bluetooth devices."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        address: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger,
            name=f"Enders Celsio {address}",
        )
        self.address = address
        self._unsub_callback: Callable[[], None] | None = None

        # Letzte bekannte Daten sofort laden
        last_info = async_last_service_info(hass, address, connectable=False)
        if last_info:
            initial_data = parse_service_info(last_info)
            if initial_data:
                self.data = initial_data

    @callback
    def async_start(self) -> Callable[[], None]:
        """Start listening for Bluetooth advertisement events."""
        if self.data is None:
            last_info = async_last_service_info(self.hass, self.address, connectable=False)
            if last_info:
                initial_data = parse_service_info(last_info)
                if initial_data:
                    self.async_set_updated_data(initial_data)

        self._unsub_callback = async_register_callback(
            self.hass,
            self._async_handle_bluetooth_event,
            BluetoothCallbackMatcher(address=self.address, connectable=False),
            BluetoothScanningMode.PASSIVE,
        )
        return self._unsub_callback

    @callback
    def _async_handle_bluetooth_event(
        self,
        service_info: BluetoothServiceInfoBleak,
        change: Any = None,
    ) -> None:
        """Handle a Bluetooth advertisement event."""
        data = parse_service_info(service_info)
        if not data:
            return

        if self.data is None:
            new_data = data
        else:
            new_data = self.data
            if data.meat_temperature is not None:
                new_data.meat_temperature = data.meat_temperature
                new_data.ambient_temperature = data.ambient_temperature
                new_data.ambient_low = data.ambient_low
                new_data.battery_level = data.battery_level
                new_data.probe_id = data.probe_id
                new_data.raw_meat = data.raw_meat
                new_data.raw_ambient = data.raw_ambient
                new_data.status_byte = data.status_byte

            if data.rssi is not None:
                new_data.rssi = data.rssi

            if data.name:
                new_data.name = data.name

            new_data.connected = True

        self.async_set_updated_data(new_data)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for Home Assistant device registry."""
        name = (
            self.data.name
            if self.data
            else f"Enders Celsio {self.address[-5:].replace(':', '')}"
        )
        model = "Celsio Wireless Meat Probe"
        if self.data and self.data.device_type == DEVICE_TYPE_BASE_STATION:
            model = "Celsio Base Station"

        return DeviceInfo(
            connections={(CONNECTION_BLUETOOTH, self.address)},
            identifiers={(DOMAIN, self.address)},
            manufacturer="Enders",
            model=model,
            name=name,
        )
