from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
import logging
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import User
from app.users import verify_user
from datetime import datetime, timedelta

# Logging config
logging.basicConfig(filename='logs/auth.log', level=logging.INFO)

#in-memory store
failed_ips = {}

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))

from datetime import datetime, timedelta

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'attempts' not in session:
        session['attempts'] = 0

    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Check if IP is blocked before anything
    if ip in failed_ips and failed_ips[ip]['count'] >= 5:
        last = failed_ips[ip]['last_attempt']
        if datetime.now() - last < timedelta(minutes=15):
            flash("Too many failed attempts from your IP. Try again later.")
            return render_template('login.html')
        else:
            # Reset IP block
            failed_ips[ip]['count'] = 0

    # Then check if session-based block is active
    if 'blocked_until' in session:
        if datetime.now() < session['blocked_until']:
            flash(f'Too many session attempts. Try again after {session["blocked_until"].strftime("%H:%M:%S")}')
            return render_template('login.html')
        else:
            session.pop('blocked_until')
            session['attempts'] = 0

    # Block session if too many attempts
    if session['attempts'] >= 5:
        session['blocked_until'] = datetime.now() + timedelta(minutes=1)
        flash('Too many failed attempts. Try again in 1 minute.')
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if verify_user(username, password):
            session['user'] = username
            session['attempts'] = 0
            logging.info(f"{datetime.now()} - SUCCESS login for user: {username} from IP: {ip}")
            return redirect(url_for('home'))

        else:
            session['attempts'] += 1
            flash('Invalid credentials')

            # Log failed attempt
            logging.warning(f"{datetime.now()} - FAILED login from IP: {ip} ({user_agent}) for user: {username}")

            # Track failed IPs
            if ip not in failed_ips:
                failed_ips[ip] = {'count': 1, 'last_attempt': datetime.now()}
            else:
                failed_ips[ip]['count'] += 1
                failed_ips[ip]['last_attempt'] = datetime.now()

            logging.warning(f"{datetime.now()} - Suspicious activity from {ip}: {failed_ips[ip]['count']} failed attempts")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Try logging in.')
            return redirect(url_for('login'))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        logging.info(f"{datetime.now()} - New registration: {username}")
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/audit')
def audit():
    if 'user' not in session or session['user'] != 'admin':
        return "Access denied"

    try:
        with open('logs/auth.log', 'r') as f:
            log_data = f.read()
    except FileNotFoundError:
        log_data = "Log file not found."

    return render_template('audit.html', logs=log_data)

@app.route('/threats')
def threats():
    if 'user' not in session or session['user'] != 'admin':
        return "Access denied"

    return render_template('threats.html', failed_ips=failed_ips)