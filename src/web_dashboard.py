from flask import Flask, redirect, url_for
from src.soil_sensor import read_sensor
from src.discord_alerts import send_discord_alert

app = Flask(__name__)

COMMAND_FILE = "manual_command.txt"
SYSTEM_FILE = "system_enabled.txt"


def get_system_status():
    try:
        with open(SYSTEM_FILE, "r") as file:
            return file.read().strip().upper()
    except FileNotFoundError:
        return "ON"


def set_system_status(status):
    with open(SYSTEM_FILE, "w") as file:
        file.write(status)

def write_command(command):
    with open(COMMAND_FILE, "w") as file:
        file.write(command)


@app.route("/")
def home():
    status = get_system_status()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plant Watering Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                padding: 20px;
                text-align: center;
            }}
            .card {{
                background: white;
                padding: 20px;
                border-radius: 12px;
                max-width: 400px;
                margin: auto;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }}
            h1 {{
                font-size: 24px;
            }}
            .status {{
                font-size: 22px;
                font-weight: bold;
                margin: 20px 0;
            }}
            button {{
                width: 100%;
                padding: 14px;
                margin: 8px 0;
                font-size: 18px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}
            .on {{
                background: #2ecc71;
                color: white;
            }}
            .off {{
                background: #e74c3c;
                color: white;
            }}
            .water {{
                background: #3498db;
                color: white;
            }}
            .stop {{
                background: #555;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Plant Watering Dashboard</h1>

            <div class="status">System: {status}</div>

            <form action="/turn-on" method="post">
                <button class="on" type="submit">Turn System ON</button>
            </form>

            <form action="/turn-off" method="post">
                <button class="off" type="submit">Turn System OFF</button>
            </form>

            <hr>

            <form action="/stats" method="get">
                <button class="water" type="submit">Show Moisture Stats</button>
            </form>


            <form action="/water/1" method="post">
                <button class="water" type="submit">Water Plant 1</button>
            </form>

            <form action="/water/2" method="post">
                <button class="water" type="submit">Water Plant 2</button>
            </form>

            <form action="/water/3" method="post">
                <button class="water" type="submit">Water Plant 3</button>
            </form>

            <form action="/water/4" method="post">
                <button class="water" type="submit">Water Plant 4</button>
            </form>

            <form action="/stop" method="post">
                <button class="stop" type="submit">Stop All Pumps</button>
            </form>
        </div>
    </body>
    </html>
    """


@app.route("/turn-on", methods=["POST"])
def turn_on():
    set_system_status("ON")
    send_discord_alert("🟢 Plant watering system turned ON. Automatic watering enabled.")
    return redirect(url_for("home"))


@app.route("/turn-off", methods=["POST"])
def turn_off():
    set_system_status("OFF")
    write_command("STOP")
    send_discord_alert("🔴 Plant watering system turned OFF. Automatic watering paused.")
    return redirect(url_for("home"))


@app.route("/water/<int:pump_number>", methods=["POST"])
def water(pump_number):
    write_command(f"WATER:{pump_number}")
    return redirect(url_for("home"))


@app.route("/stop", methods=["POST"])
def stop():
    write_command("STOP")
    return redirect(url_for("home"))


@app.route("/stats")
def stats():
    rows = ""

    for channel in range(4):
        reading = read_sensor(channel)
        moisture = reading["moisture_percent"]
        voltage = reading["voltage"]

        rows += f"""
        <p>
            <b>Plant {channel + 1}</b><br>
            Moisture: {moisture:.1f}%<br>
            Voltage: {voltage:.3f}V
        </p>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plant Stats</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                padding: 20px;
                text-align: center;
            }}
            .card {{
                background: white;
                padding: 20px;
                border-radius: 12px;
                max-width: 400px;
                margin: auto;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }}
            a {{
                display: block;
                margin-top: 20px;
                font-size: 18px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Plant Moisture Stats</h1>
            {rows}
            <a href="/">Back to Dashboard</a>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
