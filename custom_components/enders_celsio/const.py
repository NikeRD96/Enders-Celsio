"""Constants for the Enders Celsio integration."""

DOMAIN = "enders_celsio"

# Configuration
CONF_ADDRESS = "address"
CONF_DEVICE_TYPE = "device_type"

# Device Types
DEVICE_TYPE_PROBE = "probe"
DEVICE_TYPE_BASE_STATION = "base_station"

# Bluetooth Identifiers
SERVICE_UUID_CEE0 = "0000cee0-0000-1000-8000-00805f9b34fb"
NAME_PROBE_PREFIX = "WPprobe"
NAME_BASE_PREFIX = "EN2"

# Defaults
DEFAULT_NAME = "Enders Celsio"
DEFAULT_TARGET_TEMP = 56.0

# Meat Types and Doneness Presets
MEAT_TYPE_BEEF_STEAK = "beef_steak"
MEAT_TYPE_BEEF_ROAST = "beef_roast"
MEAT_TYPE_PULLED_BEEF = "pulled_beef"
MEAT_TYPE_PORK_CHOP = "pork_chop"
MEAT_TYPE_PORK_ROAST = "pork_roast"
MEAT_TYPE_PULLED_PORK = "pulled_pork"
MEAT_TYPE_POULTRY_BREAST = "poultry_breast"
MEAT_TYPE_POULTRY_WHOLE = "poultry_whole"
MEAT_TYPE_LAMB = "lamb"
MEAT_TYPE_FISH = "fish"
MEAT_TYPE_BURGER = "burger"
MEAT_TYPE_CUSTOM = "custom"

DONENESS_RARE = "rare"
DONENESS_MEDIUM_RARE = "medium_rare"
DONENESS_MEDIUM = "medium"
DONENESS_MEDIUM_WELL = "medium_well"
DONENESS_WELL_DONE = "well_done"
DONENESS_PULLED = "pulled"
DONENESS_CUSTOM = "custom"

MEAT_PRESETS: dict[str, dict[str, float]] = {
    MEAT_TYPE_BEEF_STEAK: {
        DONENESS_RARE: 50.0,
        DONENESS_MEDIUM_RARE: 54.0,
        DONENESS_MEDIUM: 58.0,
        DONENESS_MEDIUM_WELL: 62.0,
        DONENESS_WELL_DONE: 68.0,
    },
    MEAT_TYPE_BEEF_ROAST: {
        DONENESS_MEDIUM_RARE: 56.0,
        DONENESS_MEDIUM: 65.0,
        DONENESS_MEDIUM_WELL: 72.0,
        DONENESS_WELL_DONE: 80.0,
    },
    MEAT_TYPE_PULLED_BEEF: {
        DONENESS_PULLED: 94.0,
    },
    MEAT_TYPE_PORK_CHOP: {
        DONENESS_MEDIUM: 62.0,
        DONENESS_MEDIUM_WELL: 68.0,
        DONENESS_WELL_DONE: 74.0,
    },
    MEAT_TYPE_PORK_ROAST: {
        DONENESS_MEDIUM: 70.0,
        DONENESS_WELL_DONE: 80.0,
    },
    MEAT_TYPE_PULLED_PORK: {
        DONENESS_PULLED: 93.0,
    },
    MEAT_TYPE_POULTRY_BREAST: {
        DONENESS_WELL_DONE: 74.0,
    },
    MEAT_TYPE_POULTRY_WHOLE: {
        DONENESS_WELL_DONE: 82.0,
    },
    MEAT_TYPE_LAMB: {
        DONENESS_RARE: 52.0,
        DONENESS_MEDIUM_RARE: 56.0,
        DONENESS_MEDIUM: 60.0,
        DONENESS_MEDIUM_WELL: 66.0,
        DONENESS_WELL_DONE: 74.0,
    },
    MEAT_TYPE_FISH: {
        DONENESS_RARE: 48.0,
        DONENESS_MEDIUM: 54.0,
        DONENESS_WELL_DONE: 62.0,
    },
    MEAT_TYPE_BURGER: {
        DONENESS_MEDIUM_RARE: 56.0,
        DONENESS_MEDIUM: 62.0,
        DONENESS_WELL_DONE: 72.0,
    },
    MEAT_TYPE_CUSTOM: {
        DONENESS_CUSTOM: 55.0,
    },
}
