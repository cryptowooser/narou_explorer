#!/bin/bash


# Navigate to your Django project directory
cd capyscan

# Get current date in YYYY-MM-DD format
CURRENT_DATE=$(date +%Y-%m-%d)

# Run the management command with the current date
python3 manage.py fetch_daily_rankings $CURRENT_DATE