from src.plant_logic import get_plant_status


def decide_action(plant_name, moisture_percent):
    status = get_plant_status(moisture_percent)

    if status == "INVALID":
        return {
            "plant": plant_name,
            "status": status,
            "should_water": False,
            "message": f"{plant_name}: invalid moisture reading."
        }

    if status == "DRY":
        return {
            "plant": plant_name,
            "status": status,
            "should_water": True,
            "message": f"{plant_name} is dry and needs watering."
        }

    return {
        "plant": plant_name,
        "status": status,
        "should_water": False,
        "message": f"{plant_name} does not need watering."
    }