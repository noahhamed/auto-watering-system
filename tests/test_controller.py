from src.controller import decide_action


def test_dry_plant_should_water():
    result = decide_action("Plant 1", 20)

    assert result["plant"] == "Plant 1"
    assert result["status"] == "DRY"
    assert result["should_water"] is True


def test_okay_plant_should_not_water():
    result = decide_action("Plant 2", 50)

    assert result["status"] == "OKAY"
    assert result["should_water"] is False


def test_wet_plant_should_not_water():
    result = decide_action("Plant 3", 90)

    assert result["status"] == "WET"
    assert result["should_water"] is False


def test_invalid_reading_should_not_water():
    result = decide_action("Plant 4", -10)

    assert result["status"] == "INVALID"
    assert result["should_water"] is False

from src.controller import COOLDOWN_SECONDS


def test_dry_plant_does_not_water_if_tank_empty():
    result = decide_action("Plant 1", 20, tank_has_water=False)

    assert result["status"] == "DRY"
    assert result["should_water"] is False
    assert result["reason"] == "tank_empty"


def test_dry_plant_does_not_water_during_cooldown():
    result = decide_action(
        "Plant 1",
        20,
        tank_has_water=True,
        seconds_since_last_watered=60
    )

    assert result["status"] == "DRY"
    assert result["should_water"] is False
    assert result["reason"] == "cooldown_active"


def test_dry_plant_waters_after_cooldown():
    result = decide_action(
        "Plant 1",
        20,
        tank_has_water=True,
        seconds_since_last_watered=COOLDOWN_SECONDS + 1
    )

    assert result["status"] == "DRY"
    assert result["should_water"] is True
    assert result["reason"] == "dry"