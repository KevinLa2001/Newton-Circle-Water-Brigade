"""
Newton Circle Water Brigade — Universal Python Implementation

This module implements the core data models and automation logic from the Water Schedule Spec.
It is designed for clarity and maintainability, and can be adapted to any UI or automation platform.
"""
import uuid
from datetime import date, timedelta
from typing import List, Optional

# --- Data Models ---

class WateringSlot:
    def __init__(self, date_: date, is_heat_triggered=False, is_rain_day=False, rain_probability=0, high_temp=None, weather_code=None):
        self.id = str(uuid.uuid4())
        self.date = date_
        self.assigned_to: Optional[str] = None
        self.status = 'Open'  # Open, Filled, Rain, Past
        self.is_heat_triggered = is_heat_triggered
        self.is_rain_day = is_rain_day
        self.rain_probability = rain_probability
        self.high_temp = high_temp
        self.weather_code = weather_code
        self.notifications_sent = False

class User:
    def __init__(self, name: str, contact: str, is_admin=False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.contact = contact
        self.is_admin = is_admin

class AdminSettings:
    def __init__(self):
        self.rain_threshold = 80  # percent
        self.heat_threshold = 80  # deg F
        self.auto_clear_on_rain = True
        self.season_start = date(date.today().year, 5, 10)
        self.season_end = date(date.today().year, 9, 30)
        self.watering_pattern = [0, 2, 4, 5, 6]  # Mon, Wed, Fri, Sat, Sun

# --- Core Logic ---

class WateringScheduler:
    def __init__(self, settings: AdminSettings):
        self.settings = settings
        self.slots: List[WateringSlot] = []
        self.users: List[User] = []

    def generate_schedule(self):
        self.slots.clear()
        d = self.settings.season_start
        while d <= self.settings.season_end:
            if d.weekday() in self.settings.watering_pattern:
                self.slots.append(WateringSlot(date_=d))
            d += timedelta(days=1)

    def apply_rain_rule(self, forecast: dict, temp_forecast: dict = None):
        for slot in self.slots:
            if slot.date >= date.today():
                rain_prob = forecast.get(slot.date, 0)
                if rain_prob >= self.settings.rain_threshold:
                    slot.status = 'Rain'
                    slot.is_rain_day = True
                    slot.rain_probability = rain_prob
                    if self.settings.auto_clear_on_rain:
                        slot.assigned_to = None
                # Set high temperature if provided
                if temp_forecast and slot.date in temp_forecast:
                    slot.high_temp = temp_forecast[slot.date]

    def apply_heat_rule(self, forecast: dict):
        for slot in self.slots:
            if slot.date >= date.today() and not slot.is_rain_day:
                high_temp = forecast.get(slot.date, 0)
                # Set high temperature for all slots
                slot.high_temp = high_temp
                if high_temp >= self.settings.heat_threshold and slot.date.weekday() not in self.settings.watering_pattern:
                    # Add heat-triggered slot if not already present
                    self.slots.append(WateringSlot(date_=slot.date, is_heat_triggered=True, high_temp=high_temp))

    def assign_user(self, slot_date: date, user_name: str):
        for slot in self.slots:
            if slot.date == slot_date:
                slot.assigned_to = user_name
                slot.status = 'Filled'
                return True
        return False

    def remove_user(self, slot_date: date, user_name: str):
        for slot in self.slots:
            if slot.date == slot_date and slot.assigned_to == user_name:
                slot.assigned_to = None
                slot.status = 'Open'
                return True
        return False

    def get_open_slots(self):
        return [slot for slot in self.slots if slot.status == 'Open']

    def notify_users(self, message: str):
        # Placeholder for notification logic
        print(f"NOTIFY: {message}")

# --- Example Usage ---
if __name__ == "__main__":
    settings = AdminSettings()
    scheduler = WateringScheduler(settings)
    scheduler.generate_schedule()

    # Example: apply weather rules
    rain_forecast = {slot.date: 90 if slot.date.day % 7 == 0 else 10 for slot in scheduler.slots}
    heat_forecast = {slot.date: 85 if slot.date.day % 5 == 0 else 75 for slot in scheduler.slots}
    scheduler.apply_rain_rule(rain_forecast)
    scheduler.apply_heat_rule(heat_forecast)

    # Example: assign and remove users
    user = User("Alice", "alice@example.com")
    scheduler.users.append(user)
    first_open = scheduler.get_open_slots()[0]
    scheduler.assign_user(first_open.date, user.name)
    scheduler.remove_user(first_open.date, user.name)

    # Print schedule summary
    for slot in scheduler.slots[:10]:
        print(slot.date, slot.status, slot.assigned_to, slot.is_heat_triggered, slot.is_rain_day)
