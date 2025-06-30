from flask import render_template, request, redirect, url_for, session, flash
import logging
from datetime import datetime
from app import app
from app.users import verify_user

# Set up logging
logging.basicConfig(filename='logs/auth.log', level=logging.INFO)

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            session['user'] = username
            logging.info(f"{datetime.now()} - SUCCESS login for user: {username}")
            return redirect(url_for('home'))
        else:
            logging.warning(f"{datetime.now()} - FAILED login attempt for user: {username}")
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))