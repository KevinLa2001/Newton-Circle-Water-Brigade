import requests
from datetime import date, timedelta

# Example: Newton, MA coordinates
LAT = 42.337
LON = -71.209

def get_weather_forecast(target_date: date):
    """
    Fetch daily weather forecast for the given date (up to 7 days ahead) from Open-Meteo.
    Returns (rain_probability, high_temp, weather_code) or (None, None, None) if unavailable.
    """
    today = date.today()
    days_ahead = (target_date - today).days
    if days_ahead < 0 or days_ahead > 6:
        return None, None, None
    url = (
        f'https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}'
        f'&daily=precipitation_probability_max,temperature_2m_max,weather_code&forecast_days=7&timezone=auto'
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        return None, None, None
    data = resp.json()
    try:
        rain_probs = data['daily']['precipitation_probability_max']
        temps = data['daily']['temperature_2m_max']
        codes = data['daily']['weather_code']
        rain_prob = int(rain_probs[days_ahead])
        high_temp = int(temps[days_ahead])
        weather_code = int(codes[days_ahead])
        return rain_prob, high_temp, weather_code
    except Exception:
        return None, None, None
