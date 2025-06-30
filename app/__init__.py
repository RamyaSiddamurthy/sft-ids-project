# session secret key
from flask import Flask

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a secure one
from app import routes
