import time

from src.soil_sensor import read_sensor
from src.controller import decide_action
from src.pump import water_plant, stop_all_pumps
from src.discord_alerts import send_discord_alert
from src.event_logger import log_event


PLANT_NAME = "Plant 1"
SENSOR_CHANNEL = 0
TANK_HAS_WATER = True

WATERING_DURATION_SECONDS = 3
CHECK_INTERVAL_SECONDS = 10


try:
    while True:
        reading = read_sensor(SENSOR_CHANNEL)

        moisture = reading["moisture_percent"]
        voltage = reading["voltage"]

        result = decide_action(
            plant_name=PLANT_NAME,
            moisture_percent=moisture,
            tank_has_water=TANK_HAS_WATER,
            seconds_since_last_watered=None,
        )

        status_message = (
            f"{PLANT_NAME}: {moisture:.1f}% moisture "
            f"({voltage:.3f}V) -> {result['status']}"
        )

        print(status_message)
        print(result["message"])
        log_event(status_message)
        log_event(result["message"])

        if result["should_water"]:
            send_discord_alert(f"💧 {PLANT_NAME} is dry. Starting watering.")

            pump_result = water_plant(
                PLANT_NAME,
                duration_seconds=WATERING_DURATION_SECONDS,
            )

            print(pump_result["message"])
            log_event(pump_result["message"])

            if pump_result["success"]:
                send_discord_alert(f"✅ {pump_result['message']}")
            else:
                send_discord_alert(f"⚠️ {pump_result['message']}")

        print("-" * 60)
        time.sleep(CHECK_INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("Stopping one-plant system...")

finally:
    stop_all_pumps()