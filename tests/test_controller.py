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