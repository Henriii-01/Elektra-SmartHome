"""Constants and entity descriptors for the Elektra Verve integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.components.number import NumberDeviceClass, NumberEntityDescription
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.const import EntityCategory, UnitOfTemperature, UnitOfTime

DOMAIN = "elektra_verve"

DEFAULT_HOST = "192.168.4.1"
DEFAULT_SCAN_INTERVAL = 5  # seconds

MANUFACTURER = "Elektra"
MODEL = "Verve"


# ---------------------------------------------------------------------------
# Entity description mixins
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ElektraVerveSensorDescription(SensorEntityDescription):
    """Sensor entity description with value extraction."""

    value_fn: Callable[[dict[str, Any]], Any]


@dataclass(frozen=True, kw_only=True)
class ElektraVerveBinarySensorDescription(BinarySensorEntityDescription):
    """Binary sensor entity description with value extraction."""

    value_fn: Callable[[dict[str, Any]], bool]


@dataclass(frozen=True, kw_only=True)
class ElektraVerveNumberDescription(NumberEntityDescription):
    """Number entity description with value extraction and write-back."""

    value_fn: Callable[[dict[str, Any]], float | None]
    register: int
    command_fn: Callable[[float, dict[str, Any]], int]
    min_fn: Callable[[dict[str, Any]], float | None] | None = None
    max_fn: Callable[[dict[str, Any]], float | None] | None = None


@dataclass(frozen=True, kw_only=True)
class ElektraVerveSwitchDescription(SwitchEntityDescription):
    """Switch entity description with value extraction and write-back."""

    value_fn: Callable[[dict[str, Any]], bool]
    register: int
    on_fn: Callable[[dict[str, Any]], int]
    off_fn: Callable[[dict[str, Any]], int]


# ---------------------------------------------------------------------------
# Sensor descriptions (13 entities)
# ---------------------------------------------------------------------------

SENSOR_DESCRIPTIONS: tuple[ElektraVerveSensorDescription, ...] = (
    ElektraVerveSensorDescription(
        key="temp_group",
        translation_key="temp_group",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer",
        value_fn=lambda data: data.get("TEMP_GROUP"),
    ),
    ElektraVerveSensorDescription(
        key="secs_preinf",
        translation_key="secs_preinf",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:timer-sand",
        value_fn=lambda data: data.get("SECS_PREINF"),
    ),
    ElektraVerveSensorDescription(
        key="secs_distribution",
        translation_key="secs_distribution",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:coffee",
        value_fn=lambda data: data.get("SECS_DISTRIBUTION"),
    ),
    ElektraVerveSensorDescription(
        key="cups_counter",
        translation_key="cups_counter",
        native_unit_of_measurement="shots",
        icon="mdi:counter",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.get("CUPS_COUNTERS"),
    ),
    # Diagnostic sensors
    ElektraVerveSensorDescription(
        key="temp_min_group",
        translation_key="temp_min_group",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-chevron-down",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("TEMP_MIN_GROUP"),
    ),
    ElektraVerveSensorDescription(
        key="temp_max_group",
        translation_key="temp_max_group",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-chevron-up",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("TEMP_MAX_GROUP"),
    ),
    ElektraVerveSensorDescription(
        key="secs_min_preinf",
        translation_key="secs_min_preinf",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        icon="mdi:timer-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("SECS_MIN_PREINF"),
    ),
    ElektraVerveSensorDescription(
        key="secs_max_preinf",
        translation_key="secs_max_preinf",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        device_class=SensorDeviceClass.DURATION,
        icon="mdi:timer",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("SECS_MAX_PREINF"),
    ),
    ElektraVerveSensorDescription(
        key="firmware",
        translation_key="firmware",
        icon="mdi:chip",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("FW_REL"),
    ),
    ElektraVerveSensorDescription(
        key="ap_status",
        translation_key="ap_status",
        icon="mdi:wifi",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("AP_STATUS"),
    ),
    ElektraVerveSensorDescription(
        key="command_readback",
        translation_key="command_readback",
        icon="mdi:console",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.get("COMMAND"),
    ),
    ElektraVerveSensorDescription(
        key="device_time",
        translation_key="device_time",
        icon="mdi:clock-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: (
            f"{data['TIME'] >> 8:02d}:{data['TIME'] & 0xFF:02d}"
            if "TIME" in data
            else None
        ),
    ),
    ElektraVerveSensorDescription(
        key="device_date",
        translation_key="device_date",
        icon="mdi:calendar",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: (
            f"{(data['DATE'] >> 9) + 2000:04d}-"
            f"{(data['DATE'] >> 5) & 0xF:02d}-"
            f"{data['DATE'] & 0x1F:02d}"
            if "DATE" in data
            else None
        ),
    ),
)


# ---------------------------------------------------------------------------
# Binary sensor descriptions (7 entities, from STATUS_FLAGS bitmask)
# ---------------------------------------------------------------------------

BINARY_SENSOR_DESCRIPTIONS: tuple[ElektraVerveBinarySensorDescription, ...] = (
    ElektraVerveBinarySensorDescription(
        key="ready",
        translation_key="ready",
        device_class=BinarySensorDeviceClass.RUNNING,
        icon="mdi:coffee-maker",
        value_fn=lambda data: bool(data.get("STATUS_FLAGS", 0) & 0x01),
    ),
    ElektraVerveBinarySensorDescription(
        key="standby",
        translation_key="standby",
        icon="mdi:power-sleep",
        value_fn=lambda data: bool(data.get("STATUS_FLAGS", 0) & 0x02),
    ),
    ElektraVerveBinarySensorDescription(
        key="heating",
        translation_key="heating",
        device_class=BinarySensorDeviceClass.HEAT,
        icon="mdi:fire",
        value_fn=lambda data: bool(data.get("STATUS_FLAGS", 0) & 0x04),
    ),
    ElektraVerveBinarySensorDescription(
        key="wifi_connected",
        translation_key="wifi_connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        icon="mdi:wifi",
        value_fn=lambda data: bool(data.get("STATUS_FLAGS", 0) & 0x08),
    ),
    ElektraVerveBinarySensorDescription(
        key="alarm_1",
        translation_key="alarm_1",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:alert",
        value_fn=lambda data: bool(data.get("STATUS_FLAGS", 0) & 0x10),
    ),
    ElektraVerveBinarySensorDescription(
        key="alarm_2",
        translation_key="alarm_2",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:alert-circle",
        value_fn=lambda data: bool(data.get("STATUS_FLAGS", 0) & 0x20),
    ),
    ElektraVerveBinarySensorDescription(
        key="water_alarm",
        translation_key="water_alarm",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:water-alert",
        value_fn=lambda data: bool(data.get("STATUS_FLAGS", 0) & 0x100),
    ),
)


# ---------------------------------------------------------------------------
# Number descriptions (4 writable entities)
# ---------------------------------------------------------------------------

NUMBER_DESCRIPTIONS: tuple[ElektraVerveNumberDescription, ...] = (
    ElektraVerveNumberDescription(
        key="set_temp_group",
        translation_key="set_temp_group",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=NumberDeviceClass.TEMPERATURE,
        icon="mdi:thermometer-lines",
        native_step=1.0,
        native_min_value=70,
        native_max_value=95,
        register=11,
        value_fn=lambda data: data.get("SET_TEMP_GROUP"),
        command_fn=lambda value, data: int(value),
        min_fn=lambda data: data.get("TEMP_MIN_GROUP"),
        max_fn=lambda data: data.get("TEMP_MAX_GROUP"),
    ),
    ElektraVerveNumberDescription(
        key="set_secs_preinf",
        translation_key="set_secs_preinf",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        icon="mdi:timer-cog",
        native_step=1.0,
        native_min_value=0,
        native_max_value=20,
        register=12,
        value_fn=lambda data: data.get("SET_SECS_PREINF"),
        command_fn=lambda value, data: int(value),
        min_fn=lambda data: data.get("SECS_MIN_PREINF"),
        max_fn=lambda data: data.get("SECS_MAX_PREINF"),
    ),
    ElektraVerveNumberDescription(
        key="night_cycle_start",
        translation_key="night_cycle_start",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        icon="mdi:weather-night",
        native_step=1.0,
        native_min_value=0,
        native_max_value=1439,
        register=14,
        value_fn=lambda data: data.get("NIGTH_CYCLE_START", 0) & 0x7FFF,
        # Preserve enable bit (bit 15) when writing time value
        command_fn=lambda value, data: (
            (int(value) & 0x7FFF) | (data.get("NIGTH_CYCLE_START", 0) & 0x8000)
        ),
    ),
    ElektraVerveNumberDescription(
        key="night_cycle_stop",
        translation_key="night_cycle_stop",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        icon="mdi:weather-sunset-up",
        native_step=1.0,
        native_min_value=0,
        native_max_value=1439,
        register=15,
        value_fn=lambda data: data.get("NIGTH_CYCLE_STOP"),
        command_fn=lambda value, data: int(value),
    ),
)


# ---------------------------------------------------------------------------
# Switch descriptions (2 writable entities)
# ---------------------------------------------------------------------------

SWITCH_DESCRIPTIONS: tuple[ElektraVerveSwitchDescription, ...] = (
    ElektraVerveSwitchDescription(
        key="set_supply",
        translation_key="set_supply",
        icon="mdi:power",
        register=13,
        value_fn=lambda data: data.get("SET_SUPPLY") == 1,
        on_fn=lambda data: 1,
        off_fn=lambda data: 0,
    ),
    ElektraVerveSwitchDescription(
        key="night_cycle_enable",
        translation_key="night_cycle_enable",
        icon="mdi:moon-waning-crescent",
        register=14,
        value_fn=lambda data: bool(data.get("NIGTH_CYCLE_START", 0) & 0x8000),
        # Preserve time value (bits 0-14) when toggling enable bit (bit 15)
        on_fn=lambda data: (data.get("NIGTH_CYCLE_START", 0) & 0x7FFF) | 0x8000,
        off_fn=lambda data: data.get("NIGTH_CYCLE_START", 0) & 0x7FFF,
    ),
)
