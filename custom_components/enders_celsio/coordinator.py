"""Coordinator for Enders Celsio BLE devices."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
    async_last_service_info,
)
from homeassistant.components.bluetooth.passive_update_coordinator import (
    PassiveBluetoothDataUpdateCoordinator,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import CONNECTION_BLUETOOTH, DeviceInfo

from .const import (
    DEVICE_TYPE_BASE_STATION,
    DEVICE_TYPE_PROBE,
    DOMAIN,
)
from .parser import EndersCelsioData, parse_service_info

_LOGGER = logging.getLogger(__name__)


class EndersCelsioCoordinator(PassiveBluetoothDataUpdateCoordinator):
    """Coordinator for Enders Celsio Bluetooth devices."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        address: str,
        mode: BluetoothScanningMode = BluetoothScanningMode.PASSIVE,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=logger,
            address=address,
            mode=mode,
            connectable=False,
        )
        self.address = address
        self.device_data: EndersCelsioData | None = None

        # Letzte bekannte Bluetooth-Informationen sofort laden
        last_info = async_last_service_info(hass, address, connectable=False)
        if last_info:
            initial_data = parse_service_info(last_info)
            if initial_data:
                self.device_data = initial_data
                self.async_set_updated_data(initial_data)

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

        if self.device_data is None:
            self.device_data = data
        else:
            if data.meat_temperature is not None:
                self.device_data.meat_temperature = data.meat_temperature
                self.device_data.ambient_temperature = data.ambient_temperature
                self.device_data.ambient_low = data.ambient_low
                self.device_data.battery_level = data.battery_level
                self.device_data.probe_id = data.probe_id
                self.device_data.raw_meat = data.raw_meat
                self.device_data.raw_ambient = data.raw_ambient
                self.device_data.status_byte = data.status_byte

            if data.rssi is not None:
                self.device_data.rssi = data.rssi

            if data.name:
                self.device_data.name = data.name

            self.device_data.connected = True

        self.async_set_updated_data(self.device_data)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for Home Assistant device registry."""
        name = (
            self.device_data.name
            if self.device_data
            else f"Enders Celsio {self.address[-5:].replace(':', '')}"
        )
        model = "Celsio Wireless Meat Probe"
        if self.device_data and self.device_data.device_type == DEVICE_TYPE_BASE_STATION:
            model = "Celsio Base Station"

        return DeviceInfo(
            connections={(CONNECTION_BLUETOOTH, self.address)},
            identifiers={(DOMAIN, self.address)},
            manufacturer="Enders",
            model=model,
            name=name,
        )
