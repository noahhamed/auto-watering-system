from src.pump import water_plant, stop_all_pumps


try:
    for pump_number in range(1, 5):
        input(f"Press Enter to test Pump {pump_number}...")

        result = water_plant(
            plant_name=f"Test Plant {pump_number}",
            pump_number=pump_number,
            duration_seconds=2,
        )

        print(result["message"])

finally:
    stop_all_pumps()
