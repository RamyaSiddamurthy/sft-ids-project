# Secure File Transfer + Intrusion Detection System (SFT-IDS)

This is a cybersecurity-focused project to build a secure file-sharing web app with intrusion detection, user authentication, encryption, and logging features.

## Day 1 Progress:
- ✅ Project folder and virtual environment setup
- ✅ Installed libraries: Flask, JWT, bcrypt, Cryptography
- ✅ Created minimal Flask app and confirmed it runs

## Day 2 Progress:
- ✅ Implemented user login and logout routes with Flask
- ✅ Secured passwords using werkzeug.security hashing functions
- ✅ Managed user sessions with Flask’s session mechanism
- ✅ Created login and home HTML templates using Jinja2 templating
- ✅ Added logging of login attempts (success and failure) to logs/auth.log using Python’s logging module
- ✅ Implemented flash messages for invalid login feedback
- ✅ Ensured no plaintext passwords stored, enhancing security

## Day 3 Progress:
- ✅ Implemented user registration (/register route) with password hashing
- ✅ Integrated SQLite database using SQLAlchemy for storing user data
- ✅ Added brute-force login protection with session-based attempt tracking and 10-minute cooldown lockout
- ✅ Created admin-only audit page (/audit) to view login and registration logs
- ✅ Enhanced login system with attempt limits, logging success and failures
- ✅ Added flash messages for user feedback on registration, login errors, and blocks
- ✅ Tested registration, login, and audit features to ensure security and usability