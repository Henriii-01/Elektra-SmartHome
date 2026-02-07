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
2. Make sure the Home Assistant host (or the device running onboarding) is connected to that hotspot so it has a `192.168.4.x` address.
3. In Home Assistant, add the Elektra Verve integration and enter the hotspot SSID when prompted.
4. The integration checks the serial from the SSID against the device response before finishing setup.

### Connecting Home Assistant to the Elektra hotspot
- Add a Wi‑Fi connection on the host for SSID `elektra-<SERIAL_NUMBER>` while keeping your normal LAN link (Ethernet or another Wi‑Fi) active.
- If you use HA OS, add the Wi‑Fi network under Settings → System → Network. For HA Supervised/Core/Container, configure Wi‑Fi on the host (e.g., NetworkManager/nmcli) or in the VM/host networking so the HA process can reach 192.168.4.1.

Notes:
- The integration cannot configure Wi‑Fi for you; the host must already be joined to the Elektra hotspot when running the config flow.
- You only enter the SSID in the flow; the IP is fixed at `192.168.4.1`.

## Entities

### Sensors
- Brew Group Temperature - live group temperature in °C
- Pre-Infusion Duration - current programmed pre-infusion length in seconds
- Brew Time After Preinfusion - brew duration after preinfusion completes (seconds)
- Lifetime Shot Counter - total shots recorded by the machine (monotonic)
- Min/Max Brew Group Temperature - lowest/highest group temps reported since power-on
- Min/Max Pre-Infusion Duration - device-reported min/max allowable preinfusion times
- Machine Firmware Version - firmware revision reported by the board (diagnostic)
- Access Point Status - Wi-Fi AP status flags from the machine (diagnostic)
- Command Echo Register - last command code echoed by the machine (diagnostic)
- Machine Clock Time - time stored on the machine (diagnostic)
- Machine Clock Date - date stored on the machine (diagnostic)

### Binary Sensors
- Ready to Brew - machine warmed up and available
- Standby Mode - energy-saving standby state
- Heating Active - heaters currently running
- Wi-Fi Client Connected - hotspot has a connected client
- Alarm 1 (device) - board alarm flag
- Alarm 2 (device) - board alarm flag
- Water Alarm (low tank) - low/empty water condition flag

### Numbers (writeable)
- Target Brew Group Temperature (°C, bounded by device min/max)
- Target Pre-Infusion Duration (seconds, bounded by device min/max)
- Night Cycle Start (minutes from midnight, preserves enable bit)
- Night Cycle Stop (minutes from midnight)

Night cycle values are minutes past 00:00 (0-1439). Handy examples:
- 22:30 -> 1350
- 06:30 -> 390

### Switches (writeable)
- Main Supply Power
- Night Cycle Enabled (toggles enable bit while preserving start/stop times)

## Notes
- Communication stays local over the device access point.
- No cloud services are used.
