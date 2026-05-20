import os
import requests
from dotenv import load_dotenv


load_dotenv()


def send_discord_alert(message):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        return {
            "success": False,
            "message": "Discord webhook URL is missing."
        }

    try:
        response = requests.post(
            webhook_url,
            json={"content": message},
            timeout=10
        )

        if response.status_code == 204:
            return {
                "success": True,
                "message": "Discord alert sent."
            }

        return {
            "success": False,
            "message": f"Discord alert failed with status code {response.status_code}."
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "message": f"Discord alert error: {error}"
        }