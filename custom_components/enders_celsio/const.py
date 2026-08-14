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
DEFAULT_DISCONNECT_TIMEOUT = 120.0  # seconds until probe is considered unavailable
