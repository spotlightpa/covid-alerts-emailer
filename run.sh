#!/usr/bin/env bash

# Cronjob script - this shell script is intended to be executed by a cronjob to run the program
# at regular intervals. If you're NOT setting up this program to run as a cronjob you can ignore this file and
# simply execute the program as described in the README.

# Start
echo "##############################"
echo $(date '+%Y-%m-%d %H:%M:%S')
echo "Script start - COVID EMAIL ALERTS"
echo "ENV VARS:"
printenv
# This tells pipenv to use this .env file
export PIPENV_DOTENV_LOCATION="/home/dansr/projects/covid_email_alerts/.env"
# Navigate to scraper project directory
cd /home/dansr/projects/covid_email_alerts
# Run program
# Note: In this case executing path to binary due to problems with pyenv working in cron
export PYTHONPATH="/home/dansr/projects/covid_email_alerts"
~/.pyenv/versions/3.6.10/bin/pipenv run python src/covid_email_alerts.py
echo "ENV VARS:"
printenv
echo "DEFAULT PYTHON LOCATION:"
which python
echo "PYTHON VERSION"
python -V
echo "Script end"
echo ""