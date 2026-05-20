from src.plant_logic import get_plant_status, should_water


def test_dry_plant_status():
    assert get_plant_status(22) == "DRY"


def test_okay_plant_status():
    assert get_plant_status(55) == "OKAY"


def test_wet_plant_status():
    assert get_plant_status(82) == "WET"


def test_invalid_low_moisture():
    assert get_plant_status(-5) == "INVALID"


def test_invalid_high_moisture():
    assert get_plant_status(120) == "INVALID"


def test_should_water_when_dry():
    assert should_water(20) is True


def test_should_not_water_when_okay():
    assert should_water(50) is False


def test_should_not_water_when_wet():
    assert should_water(90) is False