# Documented at
# http://docs.gunicorn.org/en/latest/settings.html
import os

# Address where the app will be served at
bind = "127.0.0.1:5000"
# Change process name
name = "faceted"

workers = 1
check_config = True

# Enable logging at dir logs and pip output there
DIR = os.path.dirname(os.path.abspath(__file__))
access_logfile = os.path.join(DIR, "logs/access.log")
error_logfile = os.path.join(DIR, "logs/error.log")
capture_output = True
# Detach from the console and run in background
daemon = False

# Possible SSL setup

# 