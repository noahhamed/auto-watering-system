import time
from smbus2 import SMBus


ADS1115_ADDRESS = 0x48

CONVERSION_REGISTER = 0x00
CONFIG_REGISTER = 0x01

VOLTAGE_RANGE = 4.096
MAX_ADC_VALUE = 32768

DRY_VOLTAGE = 3.00
WET_VOLTAGE = 1.00

CHANNEL_CONFIGS = {
    0: 0xC383,  # A0
    1: 0xD383,  # A1
    2: 0xE383,  # A2
    3: 0xF383,  # A3
}


def write_config(bus, config):
    high_byte = (config >> 8) & 0xFF
    low_byte = config & 0xFF
    bus.write_i2c_block_data(ADS1115_ADDRESS, CONFIG_REGISTER, [high_byte, low_byte])


def read_raw_value(bus):
    data = bus.read_i2c_block_data(ADS1115_ADDRESS, CONVERSION_REGISTER, 2)
    raw = (data[0] << 8) | data[1]

    if raw > 32767:
        raw -= 65536

    return raw


def raw_to_voltage(raw):
    return raw * VOLTAGE_RANGE / MAX_ADC_VALUE


def voltage_to_moisture_percent(voltage):
    moisture = (DRY_VOLTAGE - voltage) / (DRY_VOLTAGE - WET_VOLTAGE) * 100
    return max(0, min(100, moisture))


def get_status(moisture_percent):
    if moisture_percent < 30:
        return "DRY"
    elif moisture_percent <= 75:
        return "OKAY"
    else:
        return "WET"


def read_channel(bus, channel):
    write_config(bus, CHANNEL_CONFIGS[channel])
    time.sleep(0.1)

    raw = read_raw_value(bus)
    voltage = raw_to_voltage(raw)
    moisture = voltage_to_moisture_percent(voltage)
    status = get_status(moisture)

    return raw, voltage, moisture, status


with SMBus(1) as bus:
    while True:
        print("Moisture readings:")

        for channel in range(4):
            raw, voltage, moisture, status = read_channel(bus, channel)

            print(
                f"Sensor {channel + 1} | "
                f"A{channel} | "
                f"Raw: {raw} | "
                f"Voltage: {voltage:.3f}V | "
                f"Moisture: {moisture:.1f}% | "
                f"Status: {status}"
            )

        print("-" * 60)
        time.sleep(10)