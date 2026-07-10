import time

from src.soil_sensor import read_sensor
from src.controller import decide_action
from src.pump import water_plant, water_plant_interruptible, stop_all_pumps
from src.discord_alerts import send_discord_alert
from src.event_logger import log_event


PLANTS = [
    {
        "name": "Plant 1",
        "sensor_channel": 0,
        "pump_number": 1,
        "watering_seconds": 4,
    },
    {
        "name": "Plant 2",
        "sensor_channel": 1,
        "pump_number": 2,
        "watering_seconds": 4,
    },
    {
        "name": "Plant 3",
        "sensor_channel": 2,
        "pump_number": 3,
        "watering_seconds": 4,
    },
    {
        "name": "Plant 4",
        "sensor_channel": 3,
        "pump_number": 4,
        "watering_seconds": 4,
    },
]

COMMAND_FILE = "manual_command.txt"
COMMAND_CHECK_SECONDS = 2
TANK_HAS_WATER = True
CHECK_INTERVAL_SECONDS = 6 * 60 * 60  # 6 hours

def is_system_enabled():
    try:
        with open("system_enabled.txt", "r") as file:
            return file.read().strip().upper() == "ON"
    except FileNotFoundError:
        return True
def get_manual_command():
    try:
        with open(COMMAND_FILE, "r") as file:
            command = file.read().strip()
        open(COMMAND_FILE, "w").close()
        return command
    except FileNotFoundError:
        return ""
def stop_command_requested():
    try:
        with open(COMMAND_FILE, "r") as file:
            command = file.read().strip().upper()

        if command == "STOP":
            open(COMMAND_FILE, "w").close()
            return True

        return False

    except FileNotFoundError:
        return False

def handle_manual_command():
    command = get_manual_command()

    if command == "":
        return

    if command == "STOP":
        print("Manual command: stop all pumps.")
        log_event("Manual command: stop all pumps.")
        stop_all_pumps()
        return

    if command.startswith("WATER:"):
        try:
            pump_number = int(command.split(":")[1])
        except ValueError:
            print("Invalid manual water command.")
            return

        print(f"Manual command: water Plant {pump_number}.")
        log_event(f"Manual command: water Plant {pump_number}.")

        result = water_plant_interruptible(
            plant_name=f"Plant {pump_number}",
            pump_number=pump_number,
            duration_seconds=3,
            should_stop=stop_command_requested,
        )

        print(result["message"])
        log_event(result["message"])

        if result["success"]:
            send_discord_alert(f"📱 Manual watering: {result['message']}")
        else:
            send_discord_alert(f"⚠️ Manual watering failed: {result['message']}")


last_auto_check = 0

try:
    while True:
        handle_manual_command()

        if not is_system_enabled():
            print("System is OFF. Automatic watering paused.")
            log_event("System is OFF. Automatic watering paused.")
            stop_all_pumps()
            time.sleep(COMMAND_CHECK_SECONDS)
            continue

        current_time = time.time()

        if current_time - last_auto_check >= CHECK_INTERVAL_SECONDS:
            print("Checking all plants...")
            log_event("Checking all plants...")

            for plant in PLANTS:
                handle_manual_command()

                if not is_system_enabled():
                    print("System was turned OFF. Stopping automatic check.")
                    log_event("System was turned OFF. Stopping automatic check.")
                    stop_all_pumps()
                    break

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
                    if not is_system_enabled():
                        print("System was turned OFF before watering. Skipping pump.")
                        log_event("System was turned OFF before watering. Skipping pump.")
                        stop_all_pumps()
                        continue

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

                    time.sleep(2)

            print("-" * 60)
            last_auto_check = current_time

        time.sleep(COMMAND_CHECK_SECONDS)

except KeyboardInterrupt:
    print("Stopping four-plant system...")

finally:
    stop_all_pumps()
