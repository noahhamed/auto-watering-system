from src.pump import water_plant


def test_water_plant_success():
    result = water_plant("Plant 1", duration_seconds=5)

    assert result["success"] is True
    assert result["message"] == "Watering Plant 1 for 5 seconds."


def test_water_plant_invalid_duration():
    result = water_plant("Plant 1", duration_seconds=0)

    assert result["success"] is False