# Enders Celsio Home Assistant Integration

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/v/release/custom-components/ha-enders-celsio?style=flat-square)](https://github.com/custom-components/ha-enders-celsio/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Custom Component für **Home Assistant** zur nahtlosen Einbindung des kabellosen Bluetooth-Grillthermometers **Enders Celsio** (Fühler `WPprobe` und Basisstation `EN2`).

---

## 🥩 Funktionen

- 📡 **Passives Bluetooth Low Energy (BLE)**: Hört direkt auf die BLE-Advertisements des Fühlers – keine aktive Kopplung nötig, kein zusätzlicher Akkuverbrauch, keine Verbindungsabbrüche.
- 🌡️ **Fleischkerntemperatur**: Live-Messwert an der Spitze mit 0,1 °C Auflösung.
- 🔥 **Garraum- / Ambient-Temperatur**: Messwert am Fühlerende außerhalb des Fleisches inklusive automatischer Erkennung des "Low"-Modus (< 50 °C).
- 🔋 **Batteriezustand**: Überwachung des Fühlerakkus in Prozent.
- 📶 **Signalstärke (RSSI)**: Zur Diagnose der Bluetooth-Verbindung.
- 🚀 **Bluetooth Auto-Discovery**: Home Assistant erkennt eingeschaltete Enders Celsio Fühler und Basisstationen automatisch.
- 🌐 **ESPHome Bluetooth Proxy kompatibel**: Funktioniert sowohl mit dem internen Bluetooth-Empfänger von Home Assistant als auch mit jedem ESPHome BLE-Proxy im Netzwerk.

---

## 📊 Entitäten

| Entität | Typ | Beschreibung |
|---|---|---|
| `sensor.<device>_meat_temperature` | Sensor (`°C`) | Fleischkerntemperatur an der Spitze |
| `sensor.<device>_ambient_temperature` | Sensor (`°C`) | Garraum-/Grilltemperatur am Ende |
| `sensor.<device>_battery` | Sensor (`%`) | Batteriestand des Fühlers |
| `sensor.<device>_rssi` | Sensor (`dBm`) | Bluetooth-Signalstärke (Diagnose) |
| `binary_sensor.<device>_ambient_low` | Binary Sensor | `on`, wenn Garraumtemperatur < 50 °C |
| `binary_sensor.<device>_connected` | Binary Sensor | `on`, wenn Daten empfangen werden |

---

## 🛠️ Installation

### Methode 1: Über HACS (Empfohlen)

1. Öffne **HACS** in Home Assistant.
2. Gehe auf **Integrationen** und klicke oben rechts auf das Drei-Punkte-Menü $\rightarrow$ **Benutzerdefinierte Repositories**.
3. Füge die URL dieses Repositories ein und wähle als Kategorie **Integration**.
4. Klicke auf **Installieren** und starte Home Assistant neu.

### Methode 2: Manuelle Installation

1. Lade das Repository herunter.
2. Kopiere den Ordner `custom_components/enders_celsio` in dein Home Assistant Konfigurationsverzeichnis (`/config/custom_components/enders_celsio`).
3. Starte Home Assistant neu.

---

## ⚙️ Einrichtung

1. Schalte das Enders Celsio Thermometer ein (aus der Ladeschale nehmen).
2. Gehe in Home Assistant auf **Einstellungen** $\rightarrow$ **Geräte & Dienste**.
3. Das Gerät wird automatisch als neues Bluetooth-Gerät vorgeschlagen. Klicke einfach auf **Konfigurieren**.
4. *(Optional)* Falls nicht automatisch gefunden: Klicke auf **Integration hinzufügen**, suche nach **Enders Celsio** und wähle die MAC-Adresse deines Geräts aus.

---

## 📱 Dashboard-Beispiel (Lovelace)

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: 🥩 Enders Celsio BBQ
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.enders_probe_meat_temperature
        name: Kerntemperatur
        min: 20
        max: 100
        needle: true
        severity:
          green: 54
          yellow: 62
          red: 72
      - type: gauge
        entity: sensor.enders_probe_ambient_temperature
        name: Garraum
        min: 50
        max: 300
        needle: true
        severity:
          green: 110
          yellow: 160
          red: 220
  - type: entities
    entities:
      - entity: sensor.enders_probe_battery
      - entity: binary_sensor.enders_probe_ambient_low
      - entity: sensor.enders_probe_rssi
```

---

## 🔔 Automations-Beispiel (Garstufen-Alarm)

```yaml
alias: "BBQ: Steak Kerntemperatur erreicht"
description: "Sendet eine Benachrichtigung, sobald die Kerntemperatur 56°C (Medium) erreicht."
trigger:
  - platform: numeric_state
    entity_id: sensor.enders_probe_meat_temperature
    above: 55.9
action:
  - service: notify.persistent_notification
    data:
      title: "🥩 Fleisch ist fertig!"
      message: "Die Kerntemperatur hat {{ states('sensor.enders_probe_meat_temperature') }} °C erreicht."
mode: single
```

---

## 📄 Lizenz

Dieses Projekt steht unter der [MIT License](LICENSE).
