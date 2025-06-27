from flask import Blueprint

app_routes = Blueprint('app_routes', __name__)

@app_routes.route("/")
def home():
    return "Secure File Transfer + IDS System"