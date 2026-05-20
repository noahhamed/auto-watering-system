from src.controller import decide_action


plants = {
    "Plant 1": 22,
    "Plant 2": 55,
    "Plant 3": 82,
    "Plant 4": -5,
}


for plant_name, moisture in plants.items():
    result = decide_action(plant_name, moisture)

    print(f"{plant_name}: {moisture}% moisture -> {result['status']}")
    print(result["message"])

    if result["should_water"]:
        print(f"Watering {plant_name} for 5 seconds...")

    print()