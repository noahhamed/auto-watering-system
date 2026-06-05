from gpiozero import OutputDevice, LED
from time import sleep


PUMP_PINS = {
    1: 17,  # IN1 / M1
    2: 27,  # IN2 / M2
    3: 22,  # IN3 / M3
    4: 23,  # IN4 / M4
}

WATERING_LED_PIN = 24

pumps = {
    pump_number: OutputDevice(pin, active_high=False, initial_value=False)
    for pump_number, pin in PUMP_PINS.items()
}

watering_led = LED(WATERING_LED_PIN)


def water_plant(plant_name, pump_number=1, duration_seconds=3):
    if pump_number not in pumps:
        return {
            "success": False,
            "message": f"Invalid pump number: {pump_number}."
        }

    if duration_seconds <= 0:
        return {
            "success": False,
            "message": f"Invalid watering duration for {plant_name}."
        }

    try:
        watering_led.on()
        pumps[pump_number].on()

        sleep(duration_seconds)

        pumps[pump_number].off()
        watering_led.off()

        return {
            "success": True,
            "message": f"Watered {plant_name} with Pump {pump_number} for {duration_seconds} seconds."
        }

    except Exception as error:
        pumps[pump_number].off()
        watering_led.off()

        return {
            "success": False,
            "message": f"Pump error for {plant_name}: {error}"
        }


def stop_all_pumps():
    for pump in pumps.values():
        pump.off()

    watering_led.off()
