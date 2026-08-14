"""Select platform for Enders Celsio integration."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    DONENESS_MEDIUM,
    DONENESS_MEDIUM_RARE,
    DONENESS_MEDIUM_WELL,
    DONENESS_PULLED,
    DONENESS_RARE,
    DONENESS_WELL_DONE,
    MEAT_PRESETS,
    MEAT_TYPE_BEEF_ROAST,
    MEAT_TYPE_BEEF_STEAK,
    MEAT_TYPE_BURGER,
    MEAT_TYPE_CUSTOM,
    MEAT_TYPE_FISH,
    MEAT_TYPE_LAMB,
    MEAT_TYPE_PORK_CHOP,
    MEAT_TYPE_PORK_ROAST,
    MEAT_TYPE_POULTRY_BREAST,
    MEAT_TYPE_POULTRY_WHOLE,
    MEAT_TYPE_PULLED_BEEF,
    MEAT_TYPE_PULLED_PORK,
)
from .coordinator import EndersCelsioCoordinator

MEAT_TYPES = [
    MEAT_TYPE_BEEF_STEAK,
    MEAT_TYPE_BEEF_ROAST,
    MEAT_TYPE_PULLED_BEEF,
    MEAT_TYPE_PORK_CHOP,
    MEAT_TYPE_PORK_ROAST,
    MEAT_TYPE_PULLED_PORK,
    MEAT_TYPE_POULTRY_BREAST,
    MEAT_TYPE_POULTRY_WHOLE,
    MEAT_TYPE_LAMB,
    MEAT_TYPE_FISH,
    MEAT_TYPE_BURGER,
    MEAT_TYPE_CUSTOM,
]

ALL_DONENESS_OPTIONS = [
    DONENESS_RARE,
    DONENESS_MEDIUM_RARE,
    DONENESS_MEDIUM,
    DONENESS_MEDIUM_WELL,
    DONENESS_WELL_DONE,
    DONENESS_PULLED,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Enders Celsio select entities."""
    coordinator: EndersCelsioCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            EndersCelsioMeatTypeSelect(coordinator),
            EndersCelsioDonenessSelect(coordinator),
        ]
    )


class EndersCelsioMeatTypeSelect(
    CoordinatorEntity[EndersCelsioCoordinator], SelectEntity
):
    """Select entity for BBQ Meat Type."""

    _attr_has_entity_name = True
    _attr_translation_key = "meat_type"
    _attr_icon = "mdi:food-steak"
    _attr_options = MEAT_TYPES

    def __init__(self, coordinator: EndersCelsioCoordinator) -> None:
        """Initialize the meat type select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.address}_meat_type"
        self._attr_device_info = coordinator.device_info

    @property
    def current_option(self) -> str:
        """Return the current meat type."""
        return self.coordinator.meat_type

    async def async_select_option(self, option: str) -> None:
        """Change the selected meat type."""
        await self.coordinator.async_set_meat_type(option)


class EndersCelsioDonenessSelect(
    CoordinatorEntity[EndersCelsioCoordinator], SelectEntity
):
    """Select entity for BBQ Doneness level."""

    _attr_has_entity_name = True
    _attr_translation_key = "doneness"
    _attr_icon = "mdi:silverware-fork-knife"

    def __init__(self, coordinator: EndersCelsioCoordinator) -> None:
        """Initialize the doneness select entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.address}_doneness"
        self._attr_device_info = coordinator.device_info

    @property
    def options(self) -> list[str]:
        """Return available doneness options for the current meat type."""
        preset = MEAT_PRESETS.get(self.coordinator.meat_type, {})
        if preset:
            return list(preset.keys())
        return ALL_DONENESS_OPTIONS

    @property
    def current_option(self) -> str:
        """Return the current doneness option."""
        return self.coordinator.doneness

    async def async_select_option(self, option: str) -> None:
        """Change the selected doneness option."""
        await self.coordinator.async_set_doneness(option)
