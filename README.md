# Elektra Verve Home Assistant Integration

Custom integration for connecting an Elektra Verve espresso machine to Home Assistant via the machine's built-in Wi-Fi access point (local only, no cloud).

## Features
- Local polling of the device at 192.168.4.1 with 5s refresh by default
- Serial validation: requires hotspot SSID `elektra-<SERIAL_NUMBER>` and verifies the serial reported by the device before creating the entry
- Telemetry: temperatures, timing, counters, firmware, AP status, command echo, device time/date
- Controls: target group temperature, pre-infusion time, night-cycle schedule, supply power, and night-cycle enable bit

## Repository layout
- custom_components/elektra_verve/: Integration code and translations
- legacy/: Legacy bridge scripts (not required for Home Assistant)
- proof_of_concept/: Early experiments

## Installation (HACS)
1. In HACS, add this repository as a custom integration source.
2. Install "Elektra Verve" from the custom repositories list.
3. Restart Home Assistant.

## Configuration
1. Power on the machine and join its Wi-Fi hotspot. The SSID must follow `elektra-<SERIAL_NUMBER>` (example: `elektra-123abc`).
2. In Home Assistant, add the Elektra Verve integration and enter the hotspot SSID when prompted.
3. The integration checks the serial from the SSID against the device response before finishing setup.

## Entities

### Sensors
- Group Temperature (Celsius)
- Pre-Infusion Time (seconds)
- Distribution Time (seconds)
- Shot Counter (total increasing)
- Min Group Temperature (diagnostic)
- Max Group Temperature (diagnostic)
- Min Pre-Infusion Time (diagnostic)
- Max Pre-Infusion Time (diagnostic)
- Firmware Version (diagnostic)
- AP Status (diagnostic)
- Command Register (diagnostic)
- Device Time (diagnostic)
- Device Date (diagnostic)

### Binary Sensors
- Ready (running state)
- Standby
- Heating
- Wi-Fi Connected
- Alarm 1
- Alarm 2
- Water Alarm

### Numbers (writeable)
- Target Group Temperature (°C, bounded by device min/max)
- Target Pre-Infusion Time (seconds, bounded by device min/max)
- Night Cycle Start (minutes, preserves enable bit)
- Night Cycle Stop (minutes)

### Switches (writeable)
- Supply (power)
- Night Cycle Enable (toggles night-cycle bit while preserving time)

## Notes
- Communication stays local over the device access point.
- No cloud services are used.
