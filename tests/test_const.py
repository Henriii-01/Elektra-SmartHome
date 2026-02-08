from custom_components.elektra_verve.const import (
    BINARY_SENSOR_DESCRIPTIONS,
    NUMBER_DESCRIPTIONS,
    SENSOR_DESCRIPTIONS,
    SWITCH_DESCRIPTIONS,
)


def _description(items, key: str):
    return next(desc for desc in items if desc.key == key)


def test_device_time_and_date_formatting():
    time_desc = _description(SENSOR_DESCRIPTIONS, "device_time")
    date_desc = _description(SENSOR_DESCRIPTIONS, "device_date")

    assert time_desc.value_fn({"TIME": (9 << 8) | 5}) == "09:05"
    assert date_desc.value_fn({"DATE": (24 << 9) | (6 << 5) | 15}) == "2024-06-15"


def test_night_cycle_start_preserves_enable_bit():
    desc = _description(NUMBER_DESCRIPTIONS, "night_cycle_start")
    data = {"NIGTH_CYCLE_START": 0x8000 | 600}

    assert desc.command_fn(300, data) == (0x8000 | 300)


def test_night_cycle_enable_preserves_time_value():
    desc = _description(SWITCH_DESCRIPTIONS, "night_cycle_enable")

    assert desc.off_fn({"NIGTH_CYCLE_START": 0x8123}) == 0x0123
    assert desc.on_fn({"NIGTH_CYCLE_START": 0x0123}) == 0x8123


def test_ready_flag_bitmask():
    desc = _description(BINARY_SENSOR_DESCRIPTIONS, "ready")

    assert desc.value_fn({"STATUS_FLAGS": 0x01}) is True
    assert desc.value_fn({"STATUS_FLAGS": 0x00}) is False
