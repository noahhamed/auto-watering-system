import time
from src.soil_sensor import read_all_sensors
from src.plant_logic import get_plant_status


while True:
    readings = read_all_sensors()

    print("Moisture readings:")

    for reading in readings:
        moisture = reading["moisture_percent"]
        status = get_plant_status(moisture)

        print(
            f"Sensor {reading['channel'] + 1} | "
            f"Voltage: {reading['voltage']:.3f}V | "
            f"Moisture: {moisture:.1f}% | "
            f"Status: {status}"
        )

    print("-" * 60)
    time.sleep(10)