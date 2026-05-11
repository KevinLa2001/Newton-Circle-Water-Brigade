import json
import os
from datetime import date
from watering_schedule import WateringSlot

SLOTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'slots.json')

def save_slots(slots):
    data = []
    for slot in slots:
        data.append({
            'date': slot.date.isoformat(),
            'assigned_to': slot.assigned_to,
            'status': slot.status,
            'is_heat_triggered': slot.is_heat_triggered,
            'is_rain_day': slot.is_rain_day,
            'rain_probability': slot.rain_probability,
            'high_temp': slot.high_temp,
            'weather_code': slot.weather_code
        })
    with open(SLOTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_slots():
    if not os.path.exists(SLOTS_FILE):
        return None
    with open(SLOTS_FILE, 'r') as f:
        data = json.load(f)
    slots = []
    for item in data:
        slot = WateringSlot(
            date_=date.fromisoformat(item['date']),
            is_heat_triggered=item.get('is_heat_triggered', False),
            is_rain_day=item.get('is_rain_day', False),
            rain_probability=item.get('rain_probability', 0),
            high_temp=item.get('high_temp'),
            weather_code=item.get('weather_code')
        )
        slot.assigned_to = item.get('assigned_to', 'N/A')
        slot.status = item.get('status', 'Open')
        slots.append(slot)
    return slots
