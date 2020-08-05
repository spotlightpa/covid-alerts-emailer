#!/usr/bin/env bash

# Cronjob script - this shell script is intended to be executed by a cronjob to run the program
# at regular intervals. If you're NOT setting up this program to run as a cronjob you can ignore this file and
# simply execute the program as described in the README.

# Start
echo "##############################"
date '+%Y-%m-%d %H:%M:%S'
echo "*** Script start - COVID EMAIL ALERTS ***"
# Get env vars for debugging purposes
echo "DEBUG INFO..."
echo "ENV VARS:"
printenv
echo "PYTHON LOCATION:"
which python
echo "PYTHON VERSION:"
python -V
echo "NAVIGATE TO PROJ DIRECTORY AND EXECUTE PROJECT..."
# This tells pipenv to use this .env file
export PIPENV_DOTENV_LOCATION="/home/dansr/projects/covid_email_alerts/.env"
# Navigate to scraper project directory
cd /home/dansr/projects/covid_email_alerts || return
# Run program
# Note: Using abs path to pipenv binary due to problems with pyenv/pipenv PATH resolution in cron
export PYTHONPATH="/home/dansr/projects/covid_email_alerts"
~/.pyenv/versions/3.6.10/bin/pipenv run python covid_email_alerts/covid_email_alerts.py
# Get env vars for debugging purposes
echo "PROGRAM RUN COMPLETE"
echo "More DEBUG INFO..."
echo "ENV VARS:"
printenv
echo "*** Script end ***"
echo ""