from src.controller import decide_action


fake_plants = {
    "Plant 1": {
        "moisture": 22,
        "seconds_since_last_watered": None,
    },
    "Plant 2": {
        "moisture": 55,
        "seconds_since_last_watered": None,
    },
    "Plant 3": {
        "moisture": 82,
        "seconds_since_last_watered": None,
    },
    "Plant 4": {
        "moisture": 20,
        "seconds_since_last_watered": 60,
    },
}

tank_has_water = True


for plant_name, plant_data in fake_plants.items():
    result = decide_action(
        plant_name=plant_name,
        moisture_percent=plant_data["moisture"],
        tank_has_water=tank_has_water,
        seconds_since_last_watered=plant_data["seconds_since_last_watered"],
    )

    print(f"{plant_name}: {plant_data['moisture']}% moisture -> {result['status']}")
    print(result["message"])

    if result["should_water"]:
        print(f"Watering {plant_name} for 5 seconds...")

    print()