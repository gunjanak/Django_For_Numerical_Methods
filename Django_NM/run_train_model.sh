#!/bin/bash

# Set environment variables (if needed)
#export DJANGO_SETTINGS_MODULE=Django_For_Numerical_Methods.settings

# Run the Django management command
/home/janak/Documents/Django_NM/venv/bin/python /home/janak/Documents/Django_NM/Django_For_Numerical_Methods/manage.py train_model >> /home/janak/Documents/Django_NM/cron.log 2>&1
