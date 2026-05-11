import json
from datetime import datetime

with open('slots.json', 'r', encoding='utf-8') as f:
    slots = json.load(f)

for slot in slots:
    try:
        date_obj = datetime.strptime(slot['date'], '%Y-%m-%d')
        if date_obj.weekday() == 5:  # Saturday (Monday=0)
            slot['assigned_to'] = 'Melissa Scott'
            slot['status'] = 'Filled'
    except Exception as e:
        print(f"Error with date {slot.get('date')}: {e}")

with open('slots.json', 'w', encoding='utf-8') as f:
    json.dump(slots, f, indent=2)
print('All Saturdays updated to Melissa Scott and Filled.')
