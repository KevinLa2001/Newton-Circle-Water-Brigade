
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from datetime import date, timedelta

bp = Blueprint('main', __name__)

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
    # Persist assignment if needed (optional: could persist slots to file)
    flash(f'Assigned {assigned_to} to {slot_date}')
    return redirect(url_for('main.calendar'))

# New user form for dropdown
@bp.route('/new_user', methods=['GET', 'POST'])
def new_user():
    slot_date = request.args.get('slot_date') or request.form.get('slot_date')
    if request.method == 'POST':
        from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
        from datetime import date, timedelta
        import sys
        import os
        import json
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from watering_schedule import WateringScheduler, AdminSettings, User

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


import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from watering_schedule import WateringScheduler, AdminSettings, User

# Persistent user storage
USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'users.json')
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            data = json.load(f)
            return [User(u['name'], u['contact']) for u in data]
    else:
        # Initial table if file missing
        initial = [
            {"name": "Octavia", "contact": "octaviagarden@gmail.com"},
            {"name": "Jon", "contact": "jonrzulauf@gmail.com"},
            {"name": "Matt", "contact": ""},
            {"name": "Nate", "contact": ""},
            {"name": "Kip", "contact": "kip.white@cbrealty.com"},
            {"name": "Greg", "contact": ""},
            {"name": "Melissa Scott", "contact": "melissa.chinn.scott@gmail.com"},
            {"name": "Kevin Larkin", "contact": "kevinla_ms@hotmail.com"}
        ]
        with open(USERS_FILE, 'w') as f:
            json.dump(initial, f, indent=2)
        return [User(u['name'], u['contact']) for u in initial]

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump([{"name": u.name, "contact": u.contact} for u in users], f, indent=2)

# Initialize scheduler and generate schedule
settings = AdminSettings()
scheduler = WateringScheduler(settings)
scheduler.generate_schedule()

# Load users from persistent storage
loaded_users = load_users()
user_names = set()
for person in loaded_users:
    if person.name not in user_names:
        scheduler.users.append(person)
        user_names.add(person.name)


# Remove static assignment loop. Assignments should persist and only change when user acts.

def get_slots():
    # For demo, just return all slots for the current season
    return scheduler.slots

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/calendar')
def calendar():
    slots = get_slots()
    users = scheduler.users
    return render_template('calendar.html', slots=slots, users=users)

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
        contact = request.form['contact']
        # Assign user to slot
        from watering_schedule import User
        user = User(name, contact)
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
        else:
            flash('No matching assignment found.')
        return redirect(url_for('main.day_detail', date_str=date_str))
    return render_template('remove.html', slot=slot)

@bp.route('/weather_update')
def weather_update():
    from weather import get_weather_forecast
    rain_forecast = {}
    heat_forecast = {}
    weather_codes = {}
    for slot in scheduler.slots:
        rain_prob, high_temp, weather_code = get_weather_forecast(slot.date)
        if rain_prob is not None:
            rain_forecast[slot.date] = rain_prob
        if high_temp is not None:
            heat_forecast[slot.date] = high_temp
        if weather_code is not None:
            slot.weather_code = weather_code
    # Pass both rain and temp forecasts to apply_rain_rule
    scheduler.apply_rain_rule(rain_forecast, temp_forecast=heat_forecast)
    scheduler.apply_heat_rule(heat_forecast)
    flash('Weather automation applied to schedule!')
    return redirect(url_for('main.calendar'))
