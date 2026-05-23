from gpiozero import OutputDevice
from time import sleep


# Most relay modules are active LOW:
# ON  = GPIO LOW
# OFF = GPIO HIGH
relay = OutputDevice(17, active_high=False, initial_value=False)


try:
    while True:
        print("Relay ON")
        relay.on()
        sleep(1)

        print("Relay OFF")
        relay.off()
        sleep(1)

except KeyboardInterrupt:
    print("Stopping relay test...")

finally:
    relay.off()