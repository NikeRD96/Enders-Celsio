"""Number platform for Enders Celsio integration."""
from __future__ import annotations

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EndersCelsioCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Enders Celsio number entities."""
    coordinator: EndersCelsioCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([EndersCelsioTargetTemperatureNumber(coordinator)])


class EndersCelsioTargetTemperatureNumber(
    CoordinatorEntity[EndersCelsioCoordinator], NumberEntity
):
    """Number entity for setting BBQ target core temperature."""

    _attr_has_entity_name = True
    _attr_translation_key = "target_temperature"
    _attr_icon = "mdi:target"
    _attr_device_class = NumberDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_native_min_value = 40.0
    _attr_native_max_value = 100.0
    _attr_native_step = 1.0
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: EndersCelsioCoordinator) -> None:
        """Initialize the target temperature number entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.address}_target_temperature"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> float:
        """Return the target temperature."""
        return self.coordinator.target_temperature

    async def async_set_native_value(self, value: float) -> None:
        """Set the target temperature."""
        await self.coordinator.async_set_target_temperature(value)
