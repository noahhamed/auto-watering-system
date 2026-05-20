from src.plant_logic import get_plant_status


COOLDOWN_SECONDS = 6 * 60 * 60  # 6 hours


def decide_action(
    plant_name,
    moisture_percent,
    tank_has_water=True,
    seconds_since_last_watered=None
):
    status = get_plant_status(moisture_percent)

    if status == "INVALID":
        return {
            "plant": plant_name,
            "status": status,
            "should_water": False,
            "reason": "invalid_reading",
            "message": f"{plant_name}: invalid moisture reading."
        }

    if status != "DRY":
        return {
            "plant": plant_name,
            "status": status,
            "should_water": False,
            "reason": "moisture_okay",
            "message": f"{plant_name} does not need watering."
        }

    if not tank_has_water:
        return {
            "plant": plant_name,
            "status": status,
            "should_water": False,
            "reason": "tank_empty",
            "message": f"{plant_name} is dry, but the water tank is empty."
        }

    if seconds_since_last_watered is not None and seconds_since_last_watered < COOLDOWN_SECONDS:
        return {
            "plant": plant_name,
            "status": status,
            "should_water": False,
            "reason": "cooldown_active",
            "message": f"{plant_name} is dry, but cooldown is still active."
        }

    return {
        "plant": plant_name,
        "status": status,
        "should_water": True,
        "reason": "dry",
        "message": f"{plant_name} is dry and needs watering."
    }