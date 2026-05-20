def water_plant(plant_name, duration_seconds=5):
    if duration_seconds <= 0:
        return {
            "success": False,
            "message": f"Invalid watering duration for {plant_name}."
        }

    return {
        "success": True,
        "message": f"Watering {plant_name} for {duration_seconds} seconds."
    }