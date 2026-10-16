import requests
from datetime import datetime
from langchain.tools import tool


# ----------------------------
# Weather Tool (Free API)
# ----------------------------
@tool
def get_weather(city: str) -> str:
    """
    Get 3-day weather forecast for any city.
    """

    # Step 1: Get coordinates using geocoding
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_data = requests.get(geo_url).json()

    if "results" not in geo_data:
        return "City not found."

    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]

    # Step 2: Get weather using coordinates
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max&forecast_days=3"

    weather_data = requests.get(weather_url).json()
    temps = weather_data["daily"]["temperature_2m_max"]
    return f"3-Day Max Temperatures in {city}: {temps}"
    

# ----------------------------
# Currency Tool
# ----------------------------

@tool
def convert_currency(amount: float) -> str:
    """
    Convert USD to INR using a free live API.
    """

    try:
        url = "https://api.frankfurter.app/latest?from=USD&to=INR"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "Currency API failed."

        data = response.json()

        rate = data.get("rates", {}).get("INR")

        if not rate:
            return "Exchange rate not found in API response."

        converted = amount * rate

        return f"{amount} USD ≈ ₹{round(converted, 2)} (Rate: {rate})"

    except Exception as e:
        return f"Currency conversion error: {str(e)}"


# ----------------------------
# Time Tool
# ----------------------------


@tool
def get_current_time() -> str:
    """
    Get current system time.
    """
    from datetime import datetime
    return str(datetime.now())

# ============================================================
# REMINDER SYSTEM — SINGLE IST IMPLEMENTATION
# ============================================================

import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from langchain.tools import tool

IST = ZoneInfo("Asia/Kolkata")

# One shared reminder list and one lock
reminders = []
reminder_lock = threading.Lock()


@tool
def set_reminder(task: str, reminder_time: str) -> str:
    """
    Schedule a reminder using Indian Standard Time.

    Format: YYYY-MM-DD HH:MM
    Example: 2026-10-16 20:30
    """

    try:
        task = task.strip()

        if not task:
            return "Please specify what you want to be reminded about."

        scheduled_time = datetime.strptime(
            reminder_time.strip(),
            "%Y-%m-%d %H:%M"
        ).replace(tzinfo=IST)

        if scheduled_time <= datetime.now(IST):
            return "Please choose a future date and time in IST."

        with reminder_lock:
            reminders.append({
                "task": task,
                "time": scheduled_time,
                "triggered": False,
            })

        return (
            "✅ Reminder scheduled successfully!\n\n"
            f"Task: {task}\n"
            f"Date and time: "
            f"{scheduled_time.strftime('%d %B %Y, %I:%M %p')} IST"
        )

    except ValueError:
        return (
            "Invalid reminder date or time. "
            "Please use YYYY-MM-DD HH:MM."
        )


@tool
def get_reminders() -> str:
    """Display all scheduled reminders using IST."""

    with reminder_lock:
        if not reminders:
            return "You don't have any scheduled reminders."

        active_reminders = [
            (index, item)
            for index, item in enumerate(reminders, start=1)
            if not item["triggered"]
        ]

        if not active_reminders:
            return "You don't have any pending reminders."

        return "\n".join(
            f"{index}. {item['task']} — "
            f"{item['time'].strftime('%d %b %Y, %I:%M %p')} IST"
            for index, item in active_reminders
        )


def check_due_reminders():
    """
    Return reminders that have reached their scheduled time.
    Each reminder is returned only once.
    """

    now = datetime.now(IST)
    due_reminders = []

    with reminder_lock:
        for item in reminders:
            if not item["triggered"] and now >= item["time"]:
                item["triggered"] = True

                due_reminders.append({
                    "task": item["task"],
                    "time": item["time"],
                })

    return due_reminders