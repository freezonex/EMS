# Energy Management System (EMS)

This repository contains the Energy Management System (EMS) designed to monitor, control, and reduce the energy consumption of industrial equipment. The system integrates seamlessly with existing infrastructures and provides real-time analytics to improve energy efficiency.

## Features

- **Real-time Energy Monitoring**: Track energy consumption in real-time across various equipment.
- **Energy Consumption Analysis**: Analyze the energy consumption data to identify trends and potential savings.
- **Automated Reporting**: Generate daily, weekly, and monthly energy consumption reports.
- **Alert System**: Get notified when energy consumption exceeds predefined thresholds.

## Technologies Used

- Django REST Framework: For building the API that handles data interactions.
- MySQL: As the database backend for storing all energy consumption records.
- React: For building an interactive front-end to display energy data.

## Installation

Follow these steps to set up the EMS on your local machine:

```bash
# Clone the repository
git clone https://github.com/freezonex/EMS
cd EMS/emspro

# Install required Python packages
pip install -r requirements.txt
```

# Set up the database (Mysql)
```bash
cd emspro
cp settings_example.py settings.py
```
Change the DATABASES section to provide information for MySQL 8.0 connection

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '******',  # Database name
        'USER': '******',  # Username used to connect MySQL 8.0
        'PASSWORD': '******',  #Password for the MySQL 8.0 user
        'HOST': '******',  # Domain or IP Address that your DB is hosted on
        'PORT': '****',  # MySQL 8.0 port         
    }
}
```

```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
python manage.py runserver
```
