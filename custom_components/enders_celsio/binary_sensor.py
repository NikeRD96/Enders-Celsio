"""Binary sensor platform for Enders Celsio integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import EndersCelsioCoordinator


@dataclass(frozen=True, kw_only=True)
class EndersCelsioBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes an Enders Celsio binary sensor entity."""

    is_on_fn: Callable[[EndersCelsioCoordinator], bool | None]


BINARY_SENSOR_DESCRIPTIONS: tuple[EndersCelsioBinarySensorEntityDescription, ...] = (
    EndersCelsioBinarySensorEntityDescription(
        key="target_reached",
        translation_key="target_reached",
        icon="mdi:check-circle",
        is_on_fn=lambda coord: coord.target_reached,
    ),
    EndersCelsioBinarySensorEntityDescription(
        key="target_almost_reached",
        translation_key="target_almost_reached",
        icon="mdi:bell-ring-outline",
        is_on_fn=lambda coord: coord.target_almost_reached,
    ),
    EndersCelsioBinarySensorEntityDescription(
        key="ambient_low",
        translation_key="ambient_low",
        icon="mdi:thermometer-low",
        is_on_fn=lambda coord: coord.data.ambient_low if coord.data else None,
    ),
    EndersCelsioBinarySensorEntityDescription(
        key="connected",
        translation_key="connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        is_on_fn=lambda coord: coord.data.connected if coord.data else None,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Enders Celsio binary sensor entities."""
    coordinator: EndersCelsioCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        EndersCelsioBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class EndersCelsioBinarySensor(
    CoordinatorEntity[EndersCelsioCoordinator], BinarySensorEntity
):
    """Representation of an Enders Celsio binary sensor."""

    entity_description: EndersCelsioBinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EndersCelsioCoordinator,
        description: EndersCelsioBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.address}_{description.key}"
        self._attr_device_info = coordinator.device_info

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.entity_description.is_on_fn(self.coordinator)

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data is not None
