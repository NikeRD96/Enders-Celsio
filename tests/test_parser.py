"""Unit tests for the Enders Celsio BLE parser."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Add custom_components/enders_celsio to sys.path
package_dir = Path(__file__).resolve().parent.parent / "custom_components" / "enders_celsio"
sys.path.insert(0, str(package_dir))

from const import (
    DEVICE_TYPE_BASE_STATION,
    DEVICE_TYPE_PROBE,
)
from parser import (
    EndersCelsioData,
    parse_raw_payload,
)


class TestEndersCelsioParser(unittest.TestCase):
    """Test cases for the Enders Celsio BLE parser."""

    def test_payload_34c_low_ambient(self) -> None:
        """Test parsing payload at 34°C meat and Low ambient."""
        raw = bytes.fromhex("FA355440F5E301010154521F800025")
        data = parse_raw_payload(raw, address="E3:F5:40:54:35:FA", name="WPprobe")
        self.assertIsNotNone(data)
        assert data is not None
        self.assertEqual(data.device_type, DEVICE_TYPE_PROBE)
        self.assertEqual(data.meat_temperature, 34.0)
        self.assertIsNone(data.ambient_temperature)
        self.assertTrue(data.ambient_low)
        self.assertEqual(data.battery_level, 82)
        self.assertEqual(data.probe_id, 1)

    def test_payload_32c_low_ambient(self) -> None:
        """Test parsing payload at 32.4°C meat and Low ambient."""
        raw = bytes.fromhex("FA355440F5E301010144521F800023")
        data = parse_raw_payload(raw, address="E3:F5:40:54:35:FA", name="WPprobe")
        self.assertIsNotNone(data)
        assert data is not None
        self.assertEqual(data.meat_temperature, 32.4)
        self.assertIsNone(data.ambient_temperature)
        self.assertTrue(data.ambient_low)
        self.assertEqual(data.battery_level, 82)

    def test_payload_48c_low_ambient(self) -> None:
        """Test parsing payload at 48.3°C meat and Low ambient."""
        raw = bytes.fromhex("FA355440F5E3010101E3521F800032")
        data = parse_raw_payload(raw, address="E3:F5:40:54:35:FA", name="WPprobe")
        self.assertIsNotNone(data)
        assert data is not None
        self.assertEqual(data.meat_temperature, 48.3)
        self.assertIsNone(data.ambient_temperature)
        self.assertTrue(data.ambient_low)

    def test_payload_36c_126c_ambient(self) -> None:
        """Test parsing payload at 36.3°C meat and 126°C ambient."""
        raw = bytes.fromhex("FA355440F5E30101016B521F03CC2B")
        data = parse_raw_payload(raw, address="E3:F5:40:54:35:FA", name="WPprobe")
        self.assertIsNotNone(data)
        assert data is not None
        self.assertEqual(data.meat_temperature, 36.3)
        self.assertFalse(data.ambient_low)
        self.assertAlmostEqual(data.ambient_temperature or 0, 126.0, delta=0.5)

    def test_payload_100c_113c_ambient(self) -> None:
        """Test parsing payload at 100°C meat and 113°C ambient."""
        raw = bytes.fromhex("FA355440F5E3010103E84F1F034466")
        data = parse_raw_payload(raw, address="E3:F5:40:54:35:FA", name="WPprobe")
        self.assertIsNotNone(data)
        assert data is not None
        self.assertEqual(data.meat_temperature, 100.0)
        self.assertFalse(data.ambient_low)
        self.assertAlmostEqual(data.ambient_temperature or 0, 113.0, delta=0.5)
        self.assertEqual(data.battery_level, 79)

    def test_bleak_13_byte_split(self) -> None:
        """Test parsing when Bleak provides 13 bytes after splitting company ID."""
        raw13 = bytes.fromhex("5440F5E30101016B521F03CC2B")
        data = parse_raw_payload(raw13, address="E3:F5:40:54:35:FA", name="WPprobe")
        self.assertIsNotNone(data)
        assert data is not None
        self.assertEqual(data.meat_temperature, 36.3)
        self.assertEqual(data.ambient_temperature, 126.0)
        self.assertFalse(data.ambient_low)

    def test_invalid_payload_length(self) -> None:
        """Test that invalid payloads return None."""
        self.assertIsNone(parse_raw_payload(b""))
        self.assertIsNone(parse_raw_payload(bytes([0x01, 0x02])))


if __name__ == "__main__":
    unittest.main()
