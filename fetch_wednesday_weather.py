import requests
from datetime import datetime, timedelta

# Newton, MA coordinates
LAT = 42.3370
LON = -71.2092

# Find next Wednesday from today

today = datetime(2026, 5, 11)
# 0=Monday, 1=Tuesday, ..., 6=Sunday
wednesday = 2

days_ahead = (wednesday - today.weekday() + 7) % 7
if days_ahead == 0:
    days_ahead = 7
next_wed = today + timedelta(days=days_ahead)

start_date = next_wed.strftime('%Y-%m-%d')
end_date = start_date

url = (
    f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
    f"&daily=precipitation_probability_max,weathercode,temperature_2m_max"
    f"&timezone=America%2FNew_York&start_date={start_date}&end_date={end_date}"
)

print(f"Fetching weather for {start_date}...")
resp = requests.get(url)
print(f"Status: {resp.status_code}")
print(resp.json())
