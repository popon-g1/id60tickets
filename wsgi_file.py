#!/usr/bin/env python3
"""
WSGI configuration for PythonAnywhere deployment.

This file should be placed at /var/www/yourusername_pythonanywhere_com_wsgi.py
on PythonAnywhere.
"""

import sys
import os
from dotenv import load_dotenv

# Add your project directory to the sys.path
path = '/home/yourusername/it-support-app'  # Update with your actual path
if path not in sys.path:
    sys.path.insert(0, path)

# Load environment variables
load_dotenv(os.path.join(path, '.env'))

# Import your Flask application
from app import app as application

if __name__ == "__main__":
    application.run()