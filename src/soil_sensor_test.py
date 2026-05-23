import time
from smbus2 import SMBus


ADS1115_ADDRESS = 0x48

CONVERSION_REGISTER = 0x00
CONFIG_REGISTER = 0x01

# ADS1115 config:
# A0 single-ended, +/-4.096V range, single-shot mode
CONFIG_A0 = 0xC383

VOLTAGE_RANGE = 4.096
MAX_ADC_VALUE = 32768

# Calibration from your real test
DRY_VOLTAGE = 3.00   # air / very dry
WET_VOLTAGE = 1.01   # wet soil


def write_config(bus):
    high_byte = (CONFIG_A0 >> 8) & 0xFF
    low_byte = CONFIG_A0 & 0xFF
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

    # Keep percentage between 0 and 100
    if moisture < 0:
        return 0

    if moisture > 100:
        return 100

    return moisture


def get_moisture_status(moisture_percent):
    if moisture_percent < 30:
        return "DRY"
    elif moisture_percent <= 75:
        return "OKAY"
    else:
        return "WET"


with SMBus(1) as bus:
    while True:
        write_config(bus)
        time.sleep(0.1)

        raw_value = read_raw_value(bus)
        voltage = raw_to_voltage(raw_value)
        moisture_percent = voltage_to_moisture_percent(voltage)
        status = get_moisture_status(moisture_percent)

        print(
            f"Raw: {raw_value} | "
            f"Voltage: {voltage:.3f}V | "
            f"Moisture: {moisture_percent:.1f}% | "
            f"Status: {status}"
        )

        time.sleep(1)