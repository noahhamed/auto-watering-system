from plant_logic import get_plant_status, should_water


plants = {
    "Plant 1": 22,
    "Plant 2": 55,
    "Plant 3": 82,
}


for plant_name, moisture in plants.items():
    status = get_plant_status(moisture)

    print(f"{plant_name}: {moisture}% moisture -> {status}")

    if should_water(moisture):
        print(f"Watering {plant_name} for 5 seconds...")
    else:
        print(f"{plant_name} does not need water.")

    print()