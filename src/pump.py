from gpiozero import OutputDevice, LED
from time import sleep


PUMP_1_PIN = 17
WATERING_LED_PIN = 27

pump_1_relay = OutputDevice(PUMP_1_PIN, active_high=False, initial_value=False)
watering_led = LED(WATERING_LED_PIN)


def water_plant(plant_name, duration_seconds=3):
    if duration_seconds <= 0:
        return {
            "success": False,
            "message": f"Invalid watering duration for {plant_name}."
        }

    try:
        watering_led.on()
        pump_1_relay.on()

        sleep(duration_seconds)

        pump_1_relay.off()
        watering_led.off()

        return {
            "success": True,
            "message": f"Watered {plant_name} for {duration_seconds} seconds."
        }

    except Exception as error:
        pump_1_relay.off()
        watering_led.off()

        return {
            "success": False,
            "message": f"Pump error for {plant_name}: {error}"
        }


def stop_all_pumps():
    pump_1_relay.off()
    watering_led.off()