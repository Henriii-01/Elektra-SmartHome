# Elektra Verve — Entity list

This file lists all entities provided by the `elektra_verve` integration with a short description and the entity identifier pattern.

Notes:
- The integration sets each entity's unique ID to: `<device-serial>_<key>` (example: `12345678_temp_group`).


## Sensors
- **Brew Group Temperature** — key: `temp_group` — unique_id: `<serial>_temp_group` — data: `TEMP_GROUP` — unit: °C
- **Pre-Infusion Duration** — key: `secs_preinf` — unique_id: `<serial>_secs_preinf` — data: `SECS_PREINF` — unit: seconds
- **Brew Time After Preinfusion** — key: `secs_distribution` — unique_id: `<serial>_secs_distribution` — data: `SECS_DISTRIBUTION` — unit: seconds
- **Lifetime Shot Counter** — key: `cups_counter` — unique_id: `<serial>_cups_counter` — data: `CUPS_COUNTERS` — unit: shots (total increasing)

### Diagnostic sensors
- **Min Brew Group Temperature** — key: `temp_min_group` — unique_id: `<serial>_temp_min_group` — data: `TEMP_MIN_GROUP` — unit: °C
- **Max Brew Group Temperature** — key: `temp_max_group` — unique_id: `<serial>_temp_max_group` — data: `TEMP_MAX_GROUP` — unit: °C
- **Min Pre-Infusion Duration** — key: `secs_min_preinf` — unique_id: `<serial>_secs_min_preinf` — data: `SECS_MIN_PREINF` — unit: seconds
- **Max Pre-Infusion Duration** — key: `secs_max_preinf` — unique_id: `<serial>_secs_max_preinf` — data: `SECS_MAX_PREINF` — unit: seconds
- **Machine Firmware Version** — key: `firmware` — unique_id: `<serial>_firmware` — data: `FW_REL`
- **Access Point Status** — key: `ap_status` — unique_id: `<serial>_ap_status` — data: `AP_STATUS`
- **Command Echo Register** — key: `command_readback` — unique_id: `<serial>_command_readback` — data: `COMMAND`
- **Machine Clock Time** — key: `device_time` — unique_id: `<serial>_device_time` — data: `TIME` (formatted HH:MM)
- **Machine Clock Date** — key: `device_date` — unique_id: `<serial>_device_date` — data: `DATE` (formatted YYYY-MM-DD)

## Binary sensors
- **Ready to Brew** — key: `ready` — unique_id: `<serial>_ready` — from `STATUS_FLAGS` bit 0
- **Standby Mode** — key: `standby` — unique_id: `<serial>_standby` — from `STATUS_FLAGS` bit 1
- **Heating Active** — key: `heating` — unique_id: `<serial>_heating` — from `STATUS_FLAGS` bit 2
- **Wi-Fi Client Connected** — key: `wifi_connected` — unique_id: `<serial>_wifi_connected` — from `STATUS_FLAGS` bit 3
- **Alarm 1 (device)** — key: `alarm_1` — unique_id: `<serial>_alarm_1` — from `STATUS_FLAGS` bit 4
- **Alarm 2 (device)** — key: `alarm_2` — unique_id: `<serial>_alarm_2` — from `STATUS_FLAGS` bit 5
- **Water Alarm (low tank)** — key: `water_alarm` — unique_id: `<serial>_water_alarm` — from `STATUS_FLAGS` bit 8

## Number (writable) entities
- **Target Brew Group Temperature** — key: `set_temp_group` — unique_id: `<serial>_set_temp_group` — register: `11` — writes integer °C — min/max from device (`TEMP_MIN_GROUP`/`TEMP_MAX_GROUP`)
- **Target Pre-Infusion Duration** — key: `set_secs_preinf` — unique_id: `<serial>_set_secs_preinf` — register: `12` — writes integer seconds — min/max from device (`SECS_MIN_PREINF`/`SECS_MAX_PREINF`)
- **Night Cycle Start (minutes from midnight)** — key: `night_cycle_start` — unique_id: `<serial>_night_cycle_start` — register: `14` — writes minutes (0–1439). Note: bit 15 of this register is the enable flag; writing preserves the enable bit.
- **Night Cycle Stop (minutes from midnight)** — key: `night_cycle_stop` — unique_id: `<serial>_night_cycle_stop` — register: `15` — writes minutes (0–1439)

## Switch (writable) entities
- **Main Supply Power** — key: `set_supply` — unique_id: `<serial>_set_supply` — register: `13` — write `1` = on, `0` = off
- **Night Cycle Enabled** — key: `night_cycle_enable` — unique_id: `<serial>_night_cycle_enable` — register: `14` (uses `NIGTH_CYCLE_START` register's bit 15) — toggles enable bit while preserving time value