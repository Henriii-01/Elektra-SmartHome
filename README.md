# Elektra Verve Home Assistant Integration

Custom integration for connecting a standalone Elektra Verve espresso machine to Home Assistant over the device's built-in access point.

## Repository layout
- custom_components/elektra_verve/: Integration code and translations
- legacy/: Legacy bridge scripts (not required for Home Assistant)
- proof_of_concept/: Early experiments

## Installation (HACS)
1. In HACS, add this repository as a custom integration source.
2. Install "Elektra Verve" from the custom repositories list.
3. Restart Home Assistant.

## Configuration
1. Power on the machine and join its WiFi hotspot. The SSID must follow `elektra_<SERIAL_NUMBER>` (example: `elektra_123456`).
2. The device always uses the fixed address `192.168.4.1`; no IP selection is needed.
3. In Home Assistant, add the Elektra Verve integration and enter the hotspot SSID when prompted.
4. The integration validates the serial from the SSID against the device response before creating the entry.

## Notes
- Communication stays local over the device access point.
- No cloud services are used.
