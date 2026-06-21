# Automated Plant Watering System

A Raspberry Pi-based system that monitors soil moisture and automatically waters plants when they are dry.

The system uses soil moisture sensors, an ADS1115 analog-to-digital converter, a relay module, and mini water pumps. It is written in Python and includes Discord alerts and event logging.

## Features

* Monitors 4 plants using soil moisture sensors
* Converts sensor readings into moisture percentages
* Controls 4 mini water pumps using a relay module
* Waters only the plants that are dry
* Sends Discord alerts when watering happens
* Logs system events for debugging and tracking

## Hardware Used

* Raspberry Pi 4
* ADS1115 ADC
* 4 capacitive soil moisture sensors
* 4-channel relay module
* 4 mini water pumps
* External battery pack for pumps
* Breadboard and jumper wires
* Water tubing
* LED watering indicator

## How It Works

The Raspberry Pi reads moisture data from the sensors through the ADS1115 ADC. The Python program checks each plant’s moisture level and turns on the matching pump if the soil is dry.

```text
Soil Sensor → ADS1115 → Raspberry Pi → Relay → Pump → Plant
```

Each plant has its own sensor and pump:

```text
Sensor A0 → Pump 1
Sensor A1 → Pump 2
Sensor A2 → Pump 3
Sensor A3 → Pump 4
```

## Main Files

```text
src/four_plant_system.py  # Main automation script
src/soil_sensor.py        # Reads moisture sensors
src/pump.py               # Controls pumps
src/controller.py         # Handles watering decisions
src/discord_alerts.py     # Sends Discord alerts
src/event_logger.py       # Logs events
```

## Running the Project

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the full system:

```bash
python -m src.four_plant_system
```

Optional hardware tests:

```bash
python -m src.read_sensors
python -m src.pump_test
```

## Environment Variables

The Discord webhook is stored in a `.env` file:

```env
DISCORD_WEBHOOK_URL=your_webhook_url_here
```

The `.env` file is ignored by Git so private keys are not uploaded to GitHub.

## Current Status

Completed:

* 4 soil moisture sensors
* 4 relay-controlled pumps
* Moisture percentage readings
* Discord alerts
* Event logging
* 4-plant automation

Planned:

* Add ultrasonic sensor for water tank level detection
* Add low-water alerts
* Improve enclosure and wiring
* Add photos and demo video

## What I Learned

This project helped me practice Raspberry Pi GPIO, I2C communication, analog-to-digital conversion, relay control, Python project structure, Linux/SSH setup, Git/GitHub, and debugging real hardware.
