"""Sensor platform for Enders Celsio integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EndersCelsioCoordinator
from .parser import EndersCelsioData


@dataclass(frozen=True, kw_only=True)
class EndersCelsioSensorEntityDescription(SensorEntityDescription):
    """Describes an Enders Celsio sensor entity."""

    value_fn: Callable[[EndersCelsioData], Any]


SENSOR_DESCRIPTIONS: tuple[EndersCelsioSensorEntityDescription, ...] = (
    EndersCelsioSensorEntityDescription(
        key="meat_temperature",
        translation_key="meat_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        icon="mdi:thermometer",
        value_fn=lambda data: data.meat_temperature,
    ),
    EndersCelsioSensorEntityDescription(
        key="ambient_temperature",
        translation_key="ambient_temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        icon="mdi:fire",
        value_fn=lambda data: data.ambient_temperature,
    ),
    EndersCelsioSensorEntityDescription(
        key="battery",
        translation_key="battery",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        icon="mdi:battery-bluetooth",
        value_fn=lambda data: data.battery_level,
    ),
    EndersCelsioSensorEntityDescription(
        key="rssi",
        translation_key="rssi",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda data: data.rssi,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Enders Celsio sensor entities."""
    coordinator: EndersCelsioCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        EndersCelsioSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class EndersCelsioSensor(CoordinatorEntity[EndersCelsioCoordinator], SensorEntity):
    """Representation of an Enders Celsio sensor."""

    entity_description: EndersCelsioSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EndersCelsioCoordinator,
        description: EndersCelsioSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.address}_{description.key}"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data is not None
