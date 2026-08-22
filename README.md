# Enders Celsio Home Assistant Integration

[![Validate](https://github.com/NikeRD96/Enders-Celsio/actions/workflows/validate.yml/badge.svg)](https://github.com/NikeRD96/Enders-Celsio/actions/workflows/validate.yml)
[![GitHub release](https://img.shields.io/github/v/release/NikeRD96/Enders-Celsio?style=flat-square)](https://github.com/NikeRD96/Enders-Celsio/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

Vollwertige Custom Integration für **Home Assistant** zur Einbindung des kabellosen Bluetooth-Grillthermometers **Enders Celsio** (Fühler `WPprobe` und Basisstation `EN2`) inklusive **digitalem Grillassistenten** (Fleischarten-Presets, Garstufen, Zieltemperatur-Regelung und Benachrichtigungen).

---

## 🚀 1-Klick Installation via HACS

Klicke auf den folgenden Button, um das Repository direkt in deiner Home Assistant Installation als benutzerdefiniertes HACS-Repository zu öffnen:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=NikeRD96&repository=Enders-Celsio&category=integration)

---

## 🥩 Funktionen

- 📡 **Passives Bluetooth Low Energy (BLE)**: Hört direkt auf die BLE-Advertisements des Fühlers – keine aktive Kopplung nötig, kein zusätzlicher Akkuverbrauch, keine Verbindungsabbrüche.
- 🌡️ **Fleischkerntemperatur**: Live-Messwert an der Spitze mit 0,1 °C Auflösung.
- 🔥 **Garraum- / Ambient-Temperatur**: Messwert am Fühlerende außerhalb des Fleisches inklusive automatischer Erkennung des "Low"-Modus (< 50 °C).
- 🍖 **Integrierter Grillassistent (Fleischart & Garstufen-Presets)**:
  - **Fleischart (`select`)**: Rind (Steak, Braten, Pulled Beef/Brisket), Schwein (Kotelett, Braten, Pulled Pork), Geflügel (Brust, Ganz), Lamm, Fisch, Burger oder Benutzerdefiniert.
  - **Garstufe (`select`)**: Rare, Medium Rare, Medium, Medium Well, Well Done, Pulled.
  - **Zielkerntemperatur (`number`)**: Passt sich automatisch dem gewählten Preset an und kann jederzeit gradgenau manuell verstellt werden.
- 🎯 **Zieltemperatur-Erkennung**:
  - `binary_sensor.<device>_target_reached`: `on`, sobald die Zielkerntemperatur erreicht ist.
  - `binary_sensor.<device>_target_almost_reached`: `on`, 2 °C vor der Zieltemperatur (ideal zum Vorbereiten oder Ruhenlassen).
  - `sensor.<device>_cooking_progress`: Garfortschritt in Prozent (0–100 %).
- 🔋 **Batteriezustand**: Überwachung des Fühlerakkus in Prozent.
- 📶 **Signalstärke (RSSI)**: Zur Diagnose der Bluetooth-Verbindung.
- 🚀 **Bluetooth Auto-Discovery**: Home Assistant erkennt eingeschaltete Enders Celsio Fühler und Basisstationen automatisch.

---

## 📊 Übersicht aller Entitäten

| Entität | Domain | Beschreibung |
|---|---|---|
| `sensor.<device>_meat_temperature` | Sensor (`°C`) | Aktuelle Fleischkerntemperatur |
| `sensor.<device>_ambient_temperature` | Sensor (`°C`) | Aktuelle Garraumtemperatur |
| `sensor.<device>_battery` | Sensor (`%`) | Batterieladezustand des Fühlers |
| `sensor.<device>_cooking_progress` | Sensor (`%`) | Garfortschritt von Start- bis Zieltemperatur |
| `sensor.<device>_rssi` | Sensor (`dBm`) | Bluetooth-Signalstärke |
| `select.<device>_meat_type` | Select | Auswahl der Fleischart (Rind, Schwein, Geflügel, etc.) |
| `select.<device>_doneness` | Select | Auswahl der Garstufe (Rare, Medium, Well Done, etc.) |
| `number.<device>_target_temperature` | Number (`°C`) | Einstellbare Zielkerntemperatur (40–100 °C) |
| `binary_sensor.<device>_target_reached` | Binary Sensor | `on`, wenn Fleisch fertig gegart ist |
| `binary_sensor.<device>_target_almost_reached` | Binary Sensor | `on`, 2 °C vor Zieltemperatur |
| `binary_sensor.<device>_ambient_low` | Binary Sensor | `on`, wenn Garraumtemperatur < 50 °C ist |
| `binary_sensor.<device>_connected` | Binary Sensor | `on`, wenn Daten empfangen werden |

---

## 🛠️ Installation

### Methode 1: Über HACS (Empfohlen)

1. Öffne **HACS** in Home Assistant.
2. Gehe auf **Integrationen** und klicke oben rechts auf das Drei-Punkte-Menü $\rightarrow$ **Benutzerdefinierte Repositories**.
3. Füge folgende URL ein:
   ```text
   https://github.com/NikeRD96/Enders-Celsio
   ```
4. Wähle als Kategorie **Integration**.
5. Klicke auf **Hinzufügen**, suche nach **Enders Celsio**, installiere die Integration und starte Home Assistant neu.

### Methode 2: Manuelle Installation

1. Lade das neueste Release `enders_celsio.zip` von der [Releases-Seite](https://github.com/NikeRD96/Enders-Celsio/releases) herunter.
2. Entpacke das Archiv und kopiere den Ordner `enders_celsio` in dein Home Assistant Verzeichnis:
   ```text
   /config/custom_components/enders_celsio
   ```
3. Starte Home Assistant neu.

---

## ⚙️ Konfiguration

1. Sobald dein Enders Celsio Fühler eingeschaltet ist, erscheint er in Home Assistant automatisch unter **Einstellungen** $\rightarrow$ **Geräte & Dienste** via Bluetooth-Discovery.
2. Klicke auf **Konfigurieren** und bestätige das Hinzufügen.
3. Alternativ kannst du die Integration auch manuell hinzufügen: **Integration hinzufügen** $\rightarrow$ **Enders Celsio** auswählen.

---

## 📱 Dashboard-Beispiel (Lovelace BBQ Cockpit)

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: 🥩 Enders Celsio BBQ Cockpit
    subtitle: Grillassistent & Temperaturüberwachung
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
    title: 🎯 Grillassistent Einstellungen
    entities:
      - entity: select.enders_probe_meat_type
      - entity: select.enders_probe_doneness
      - entity: number.enders_probe_target_temperature
      - entity: sensor.enders_probe_cooking_progress
      - entity: binary_sensor.enders_probe_target_reached
      - entity: binary_sensor.enders_probe_target_almost_reached
      - entity: sensor.enders_probe_battery
```

---

## 🔔 Automations-Beispiel (Smartphone Push mit Ton)

```yaml
alias: "BBQ: Steak ist fertig!"
description: "Sendet eine Benachrichtigung auf das Smartphone, sobald die gewählte Garstufe erreicht ist."
trigger:
  - platform: state
    entity_id: binary_sensor.enders_probe_target_reached
    to: "on"
action:
  - action: notify.notify
    data:
      title: "🥩 Fleisch ist fertig gegart!"
      message: "Die Zielkerntemperatur ({{ states('number.enders_probe_target_temperature') }} °C) wurde erreicht. Guten Appetit!"
      data:
        push:
          sound:
            name: default
            critical: 1
            volume: 1.0
mode: single
```

---

## 📄 Lizenz

Dieses Projekt steht unter der [MIT License](LICENSE).
