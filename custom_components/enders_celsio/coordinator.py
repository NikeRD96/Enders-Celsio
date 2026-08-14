"""Coordinator for Enders Celsio BLE devices."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.bluetooth import (
    BluetoothScanningMode,
    BluetoothServiceInfoBleak,
)
from homeassistant.components.bluetooth.passive_update_coordinator import (
    PassiveBluetoothDataUpdateCoordinator,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import CONNECTION_BLUETOOTH, DeviceInfo

from .const import (
    DEFAULT_DISCONNECT_TIMEOUT,
    DEVICE_TYPE_BASE_STATION,
    DEVICE_TYPE_PROBE,
    DOMAIN,
)
from .parser import EndersCelsioData, parse_service_info

_LOGGER = logging.getLogger(__name__)


class EndersCelsioCoordinator(PassiveBluetoothDataUpdateCoordinator[EndersCelsioData]):
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
            poll_interval=None,
        )
        self.address = address
        self.device_data: EndersCelsioData | None = None

    def _async_handle_bluetooth_event(
        self,
        service_info: BluetoothServiceInfoBleak,
        change: Any = None,
    ) -> None:
        """Handle a Bluetooth advertisement event."""
        data = parse_service_info(service_info)
        if data:
            self.device_data = data
            self.async_set_updated_data(data)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for Home Assistant device registry."""
        name = self.device_data.name if self.device_data else f"Enders Celsio {self.address[-5:].replace(':', '')}"
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
