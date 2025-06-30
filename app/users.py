# app/users.py
from werkzeug.security import generate_password_hash, check_password_hash

# Simulated user "database"
users = {
    "admin": generate_password_hash("admin123")
}

def verify_user(username, password):
    if username in users and check_password_hash(users[username], password):
        return True
    return False