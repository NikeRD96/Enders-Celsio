"""Parser for Enders Celsio BLE advertisements."""
from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

try:
    from .const import (
        DEVICE_TYPE_BASE_STATION,
        DEVICE_TYPE_PROBE,
        NAME_BASE_PREFIX,
        NAME_PROBE_PREFIX,
    )
except ImportError:
    from const import (
        DEVICE_TYPE_BASE_STATION,
        DEVICE_TYPE_PROBE,
        NAME_BASE_PREFIX,
        NAME_PROBE_PREFIX,
    )

_LOGGER = logging.getLogger(__name__)


@dataclass
class EndersCelsioData:
    """Parsed data from an Enders Celsio BLE device."""

    address: str
    name: str
    device_type: str
    probe_id: int | None = None
    meat_temperature: float | None = None
    ambient_temperature: float | None = None
    ambient_low: bool = False
    battery_level: int | None = None
    rssi: int | None = None
    raw_meat: int | None = None
    raw_ambient: int | None = None
    status_byte: int | None = None
    connected: bool = True


def parse_raw_payload(payload: bytes, address: str = "", name: str = "", rssi: int | None = None) -> EndersCelsioData | None:
    """Parse raw manufacturer bytes from an Enders Celsio probe or base station.

    Supports:
    - 15-byte full manufacturer data starting with 6-byte reverse MAC:
      [0..5]: MAC reverse
      [6]: Probe ID
      [7]: Mode/Status
      [8..9]: Meat temp (Big-Endian uint16 / 10.0)
      [10]: Battery percentage
      [11]: Device subtype (0x1F)
      [12..13]: Ambient temp (0x8000 = Low, else raw ADC)
      [14]: Extra status / checksum
    - 13-byte manufacturer data (when first 2 bytes were split by Bleak as company ID)
    """
    if not payload:
        return None

    length = len(payload)
    if length == 15:
        probe_id = payload[6]
        status_byte = payload[7]
        raw_meat = (payload[8] << 8) | payload[9]
        battery = payload[10]
        raw_ambient = (payload[12] << 8) | payload[13]
    elif length == 13:
        probe_id = payload[4]
        status_byte = payload[5]
        raw_meat = (payload[6] << 8) | payload[7]
        battery = payload[8]
        raw_ambient = (payload[10] << 8) | payload[11]
    else:
        return None

    # Calculate Meat Core Temperature (0.1°C resolution)
    meat_temp = round(raw_meat / 10.0, 1)

    # Calculate Ambient Temperature
    # 0x8000 means Ambient is Low (< 50°C)
    if raw_ambient == 0x8000:
        ambient_temp = None
        ambient_low = True
    else:
        ambient_low = False
        # Calibrated formula based on empirical probe sensor points
        # (836 -> 113.0°C, 972 -> 126.0°C)
        ambient_temp = round(0.095588 * raw_ambient + 33.088, 1)

    # Battery percentage bounds
    battery_level = battery if 0 <= battery <= 100 else None

    device_name = name or (f"Enders Probe {address[-5:].replace(':', '')}" if address else "Enders Probe")

    return EndersCelsioData(
        address=address,
        name=device_name,
        device_type=DEVICE_TYPE_PROBE,
        probe_id=probe_id,
        meat_temperature=meat_temp,
        ambient_temperature=ambient_temp,
        ambient_low=ambient_low,
        battery_level=battery_level,
        rssi=rssi,
        raw_meat=raw_meat,
        raw_ambient=raw_ambient,
        status_byte=status_byte,
        connected=True,
    )


def parse_service_info(service_info: Any) -> EndersCelsioData | None:
    """Parse a Home Assistant BluetoothServiceInfoBleak or similar object."""
    address = getattr(service_info, "address", "")
    name = getattr(service_info, "name", "") or ""
    rssi = getattr(service_info, "rssi", None)
    mfr_data = getattr(service_info, "manufacturer_data", {})

    # Check manufacturer data entries
    if isinstance(mfr_data, dict):
        for company_id, data in mfr_data.items():
            if not isinstance(data, (bytes, bytearray)):
                continue

            # Try parsing with company_id prepended (15 bytes)
            if len(data) == 13:
                # Reconstruct full 15 bytes
                comp_bytes = company_id.to_bytes(2, byteorder="little")
                full_payload = comp_bytes + bytes(data)
                result = parse_raw_payload(full_payload, address=address, name=name, rssi=rssi)
                if result:
                    return result

            # Try direct payload parse
            result = parse_raw_payload(bytes(data), address=address, name=name, rssi=rssi)
            if result:
                return result

    # Check if this is the base station (EN2)
    if name.startswith(NAME_BASE_PREFIX) or address:
        # Base station advertisement without probe telemetry
        return EndersCelsioData(
            address=address,
            name=name or f"Enders Base {address[-5:].replace(':', '')}",
            device_type=DEVICE_TYPE_BASE_STATION,
            rssi=rssi,
            connected=True,
        )

    return None
