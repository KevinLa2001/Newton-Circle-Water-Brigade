from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
import sys
import os
import json
import time
from datetime import date, timedelta, datetime
from .slot_persistence import save_slots, load_slots
from watering_schedule import WateringScheduler, AdminSettings, User

bp = Blueprint('main', __name__)

@bp.route("/")
def root():
    return redirect(url_for("main.calendar"))

# Persistent user storage
USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'users.json')
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            data = json.load(f)
            return [User(u['name'], u['contacts']) for u in data]
    return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump([{"name": u.name, "contacts": [u.contacts[0]]} for u in users], f, indent=2)

def get_slots():
    return scheduler.slots

# Initialize scheduler and generate schedule
settings = AdminSettings()
scheduler = WateringScheduler(settings)
persisted_slots = load_slots()
if persisted_slots:
    scheduler.slots = persisted_slots
loaded_users = load_users()
for person in loaded_users:
    scheduler.users.append(person)

# Assign user to slot from dropdown
@bp.route('/assign_user', methods=['POST'])
def assign_user():
    slot_date = request.form['slot_date']
    assigned_to = request.form['assigned_to']
    if assigned_to == '__new__':
        # Redirect to new user form, passing slot_date
        return redirect(url_for('main.new_user', slot_date=slot_date))
    # Assign user to slot
    slot_date_obj = date.fromisoformat(slot_date)
    scheduler.assign_user(slot_date_obj, assigned_to)
    # Persist slot assignments
    save_slots(scheduler.slots)
    flash(f'Assigned {assigned_to} to {slot_date}')
    return redirect(url_for('main.calendar'))

# New user form for dropdown
@bp.route('/new_user', methods=['GET', 'POST'])
def new_user():
    slot_date = request.args.get('slot_date') or request.form.get('slot_date')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name, email)
        scheduler.users.append(user)
        save_users(scheduler.users)
        # Assign new user to slot
        slot_date_obj = date.fromisoformat(slot_date)
        scheduler.assign_user(slot_date_obj, name)
        flash(f'Added and assigned {name} to {slot_date}')
        return redirect(url_for('main.calendar'))
    return render_template('new_user.html', slot_date=slot_date)



@bp.route('/calendar')
def calendar():
    # Only update weather if more than 1 hour has passed since last update
    WEATHER_CACHE_FILE = os.path.join(os.path.dirname(__file__), '..', 'weather_last_update.txt')
    now = time.time()
    last_update = 0
    if os.path.exists(WEATHER_CACHE_FILE):
        try:
            with open(WEATHER_CACHE_FILE, 'r') as f:
                last_update = float(f.read().strip())
        except Exception:
            last_update = 0
    if now - last_update > 4 * 3600:
        from weather import get_weather_forecast
        rain_forecast = {}
        heat_forecast = {}
        for slot in scheduler.slots:
            rain_prob, high_temp, weather_code = get_weather_forecast(slot.date)
            slot.rain_probability = rain_prob if rain_prob is not None else 0
            slot.high_temp = high_temp if high_temp is not None else None
            slot.weather_code = weather_code if weather_code is not None else None
            if rain_prob is not None:
                rain_forecast[slot.date] = rain_prob
            if high_temp is not None:
                heat_forecast[slot.date] = high_temp
        scheduler.apply_rain_rule(rain_forecast, temp_forecast=heat_forecast)
        scheduler.apply_heat_rule(heat_forecast)
        save_slots(scheduler.slots)
        with open(WEATHER_CACHE_FILE, 'w') as f:
            f.write(str(now))
        flash('Weather was automatically updated for the schedule.')
    slots = get_slots()
    users = scheduler.users
    today = datetime.now().date()
    return render_template('calendar.html', slots=slots, users=users, today=today, timedelta=timedelta)

@bp.route('/day/<date_str>')
def day_detail(date_str):
    slots = get_slots()
    try:
        slot = next(s for s in slots if str(s.date) == date_str)
    except StopIteration:
        abort(404)
    return render_template('day_detail.html', slot=slot)

# User sign-up for a watering slot
@bp.route('/signup/<date_str>', methods=['GET', 'POST'])
def signup(date_str):
    slots = get_slots()
    try:
        slot = next(s for s in slots if str(s.date) == date_str)
    except StopIteration:
        abort(404)
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form.get('contact', '')
        # Assign user to slot
        from watering_schedule import User
        user = User(name, [contact])
        scheduler.users.append(user)
        scheduler.assign_user(slot.date, user.name)
        flash('You have signed up!')
        return redirect(url_for('main.day_detail', date_str=date_str))
    return render_template('signup.html', slot=slot)

# User removal from a watering slot
@bp.route('/remove/<date_str>', methods=['GET', 'POST'])
def remove(date_str):
    slots = get_slots()
    try:
        slot = next(s for s in slots if str(s.date) == date_str)
    except StopIteration:
        abort(404)
    if request.method == 'POST':
        name = request.form['name']
        # Remove user from slot
        removed = scheduler.remove_user(slot.date, name)
        if removed:
            flash('You have been removed from this slot.')
    rain_forecast = {}
    # Pass both rain and temp forecasts to apply_rain_rule
    scheduler.apply_rain_rule(rain_forecast, temp_forecast=heat_forecast)
    scheduler.apply_heat_rule(heat_forecast)
    # Save updated slots to slots.json
    save_slots(scheduler.slots)
    flash('Weather automation applied to schedule!')
    return redirect(url_for('main.calendar'))

@bp.route('/weather_update', methods=['GET', 'POST'])
def weather_update():
    # Only update weather if more than 1 hour has passed since last update
    WEATHER_CACHE_FILE = os.path.join(os.path.dirname(__file__), '..', 'weather_last_update.txt')
    now = time.time()
    last_update = 0
    if os.path.exists(WEATHER_CACHE_FILE):
        try:
            with open(WEATHER_CACHE_FILE, 'r') as f:
                last_update = float(f.read().strip())
        except Exception:
            last_update = 0
    if now - last_update > 4 * 3600:
        from weather import get_weather_forecast
        rain_forecast = {}
        heat_forecast = {}
        for slot in scheduler.slots:
            rain_prob, high_temp, weather_code = get_weather_forecast(slot.date)
            slot.rain_probability = rain_prob if rain_prob is not None else 0
            slot.high_temp = high_temp if high_temp is not None else None
            slot.weather_code = weather_code if weather_code is not None else None
            if rain_prob is not None:
                rain_forecast[slot.date] = rain_prob
            if high_temp is not None:
                heat_forecast[slot.date] = high_temp
        scheduler.apply_rain_rule(rain_forecast, temp_forecast=heat_forecast)
        scheduler.apply_heat_rule(heat_forecast)
        save_slots(scheduler.slots)
        with open(WEATHER_CACHE_FILE, 'w') as f:
            f.write(str(now))
        flash('Weather was automatically updated for the schedule.')
    else:
        flash('Weather was recently updated. Please try again later.')
    return redirect(url_for('main.calendar'))
