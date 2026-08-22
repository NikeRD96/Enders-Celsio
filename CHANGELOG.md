# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-23

### Added
- **Passive Bluetooth Low Energy (BLE)** monitoring for Enders Celsio meat thermometers (no active pairing needed, energy efficient).
- Support for **Probe (`WPprobe`)** and **Base Station (`EN2`)**.
- Core sensors:
  - Meat core temperature (`sensor.<device>_meat_temperature`)
  - Ambient / BBQ chamber temperature (`sensor.<device>_ambient_temperature`)
  - Battery percentage (`sensor.<device>_battery`)
  - Cooking progress percentage (`sensor.<device>_cooking_progress`)
  - Bluetooth RSSI signal strength (`sensor.<device>_rssi`)
- Smart BBQ Assistant:
  - Meat type selector (`select.<device>_meat_type`) with presets for Beef, Pork, Poultry, Lamb, Fish, Burger, and Custom.
  - Doneness selector (`select.<device>_doneness`) with automatic target temperature calculation (Rare, Medium Rare, Medium, Medium Well, Well Done, Pulled).
  - Target temperature control (`number.<device>_target_temperature`).
  - Binary sensors for target reached (`binary_sensor.<device>_target_reached`) and almost reached (`binary_sensor.<device>_target_almost_reached`).
  - Ambient low indicator (`binary_sensor.<device>_ambient_low`) for temperatures < 50 °C.
  - Connection indicator (`binary_sensor.<device>_connected`).
- Bluetooth auto-discovery via Home Assistant Bluetooth integration.
- Full UI configuration flow (`config_flow`) with English and German translations.
- Automation Blueprint for smartphone push notifications when meat is almost done / ready.
- Comprehensive unit test suite for BLE raw payload parsing.
- HACS custom repository compatibility.
