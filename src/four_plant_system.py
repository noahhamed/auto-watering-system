import time

from src.soil_sensor import read_sensor
from src.controller import decide_action
from src.pump import water_plant, stop_all_pumps
from src.discord_alerts import send_discord_alert
from src.event_logger import log_event


PLANTS = [
    {
        "name": "Plant 1",
        "sensor_channel": 0,
        "pump_number": 1,
        "watering_seconds": 6,
    },
    {
        "name": "Plant 2",
        "sensor_channel": 1,
        "pump_number": 2,
        "watering_seconds": 6,
    },
    {
        "name": "Plant 3",
        "sensor_channel": 2,
        "pump_number": 3,
        "watering_seconds": 6,
    },
    {
        "name": "Plant 4",
        "sensor_channel": 3,
        "pump_number": 4,
        "watering_seconds": 6,
    },
]

TANK_HAS_WATER = True
CHECK_INTERVAL_SECONDS = 10  # 6 hours


try:
    while True:
        print("Checking all plants...")
        log_event("Checking all plants...")

        for plant in PLANTS:
            reading = read_sensor(plant["sensor_channel"])

            moisture = reading["moisture_percent"]
            voltage = reading["voltage"]

            result = decide_action(
                plant_name=plant["name"],
                moisture_percent=moisture,
                tank_has_water=TANK_HAS_WATER,
                seconds_since_last_watered=None,
            )

            status_message = (
                f"{plant['name']}: {moisture:.1f}% moisture "
                f"({voltage:.3f}V) -> {result['status']}"
            )

            print(status_message)
            print(result["message"])
            log_event(status_message)
            log_event(result["message"])

            if result["should_water"]:
                send_discord_alert(
                    f"💧 {plant['name']} is dry. Starting Pump {plant['pump_number']}."
                )

                pump_result = water_plant(
                    plant_name=plant["name"],
                    pump_number=plant["pump_number"],
                    duration_seconds=plant["watering_seconds"],
                )

                print(pump_result["message"])
                log_event(pump_result["message"])

                if pump_result["success"]:
                    send_discord_alert(f"✅ {pump_result['message']}")
                else:
                    send_discord_alert(f"⚠️ {pump_result['message']}")

                # Small delay so pumps never overlap
                time.sleep(2)

        print("-" * 60)
        time.sleep(CHECK_INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("Stopping four-plant system...")

finally:
    stop_all_pumps()
