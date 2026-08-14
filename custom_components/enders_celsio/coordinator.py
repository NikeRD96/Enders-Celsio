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
    DEFAULT_TARGET_TEMP,
    DEVICE_TYPE_BASE_STATION,
    DEVICE_TYPE_PROBE,
    DOMAIN,
    DONENESS_MEDIUM,
    DONENESS_MEDIUM_RARE,
    MEAT_PRESETS,
    MEAT_TYPE_BEEF_STEAK,
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

        # BBQ Target & Preset state
        self.meat_type: str = MEAT_TYPE_BEEF_STEAK
        self.doneness: str = DONENESS_MEDIUM_RARE
        self.target_temperature: float = MEAT_PRESETS[MEAT_TYPE_BEEF_STEAK].get(
            DONENESS_MEDIUM_RARE, DEFAULT_TARGET_TEMP
        )
        self.start_temperature: float | None = None

        # Load initial data if available
        last_info = async_last_service_info(hass, address, connectable=False)
        if last_info:
            initial_data = parse_service_info(last_info)
            if initial_data:
                self.data = initial_data
                if initial_data.meat_temperature is not None:
                    self.start_temperature = initial_data.meat_temperature

    @callback
    def async_start(self) -> Callable[[], None]:
        """Start listening for Bluetooth advertisement events."""
        if self.data is None:
            last_info = async_last_service_info(self.hass, self.address, connectable=False)
            if last_info:
                initial_data = parse_service_info(last_info)
                if initial_data:
                    if initial_data.meat_temperature is not None and self.start_temperature is None:
                        self.start_temperature = initial_data.meat_temperature
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
            if data.meat_temperature is not None and self.start_temperature is None:
                self.start_temperature = data.meat_temperature
        else:
            new_data = self.data
            if data.meat_temperature is not None:
                if self.start_temperature is None:
                    self.start_temperature = data.meat_temperature
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

    async def async_set_meat_type(self, meat_type: str) -> None:
        """Set the meat type and update target temperature according to preset."""
        self.meat_type = meat_type
        available_doneness = MEAT_PRESETS.get(meat_type, {})

        if self.doneness not in available_doneness:
            # Pick first available doneness for this meat type
            self.doneness = next(iter(available_doneness.keys()), DONENESS_MEDIUM)

        self.target_temperature = available_doneness.get(self.doneness, self.target_temperature)
        if self.data:
            self.async_set_updated_data(self.data)
        else:
            self.async_update_listeners()

    async def async_set_doneness(self, doneness: str) -> None:
        """Set the doneness and update target temperature."""
        self.doneness = doneness
        available_doneness = MEAT_PRESETS.get(self.meat_type, {})
        if doneness in available_doneness:
            self.target_temperature = available_doneness[doneness]

        if self.data:
            self.async_set_updated_data(self.data)
        else:
            self.async_update_listeners()

    async def async_set_target_temperature(self, target: float) -> None:
        """Set a custom target temperature directly."""
        self.target_temperature = round(target, 1)
        if self.data:
            self.async_set_updated_data(self.data)
        else:
            self.async_update_listeners()

    @property
    def target_reached(self) -> bool:
        """Return True if meat temperature has reached target."""
        if not self.data or self.data.meat_temperature is None:
            return False
        return self.data.meat_temperature >= self.target_temperature

    @property
    def target_almost_reached(self) -> bool:
        """Return True if meat temperature is within 2°C of target."""
        if not self.data or self.data.meat_temperature is None:
            return False
        return (self.target_temperature - 2.0) <= self.data.meat_temperature < self.target_temperature

    @property
    def cooking_progress(self) -> float:
        """Return estimated cooking progress percentage (0 - 100%)."""
        if not self.data or self.data.meat_temperature is None:
            return 0.0

        meat_t = self.data.meat_temperature
        start_t = self.start_temperature if self.start_temperature is not None else 20.0
        target_t = self.target_temperature

        if target_t <= start_t:
            return 100.0 if meat_t >= target_t else 0.0

        progress = ((meat_t - start_t) / (target_t - start_t)) * 100.0
        return round(min(100.0, max(0.0, progress)), 1)

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
