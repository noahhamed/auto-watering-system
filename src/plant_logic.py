DRY_THRESHOLD = 30
WET_THRESHOLD = 75


def get_plant_status(moisture_percent):
    if moisture_percent < 0 or moisture_percent > 100:
        return "INVALID"

    if moisture_percent < DRY_THRESHOLD:
        return "DRY"
    elif moisture_percent <= WET_THRESHOLD:
        return "OKAY"
    else:
        return "WET"


def should_water(moisture_percent):
    return get_plant_status(moisture_percent) == "DRY"