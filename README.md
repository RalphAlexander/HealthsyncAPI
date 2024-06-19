# HealthsyncAPI
HealthsyncAPI is a RESTful API designed to manage and synchronize health-related data for healthcare applications. The API has an easy to use interface to handle all data with different levels of access (employees and patients level access), allowing healthcare providers to efficiently manage their records. This project is built with Python and utilizes a PostgreSQL database for data storage.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)

## Installation
1. **Clone the repo**
```
git clone https://github.com/RalphAlexander/HealthsyncAPI
```
2. **Navigate to the project directory:**
```
cd HealthsyncAPI
```
3. **Install dotenv and psycopg2**
   
Make sure you have Python and pip installed, then run:
```
pip install python-dotenv
pip install psycopg2
```
4. **Create the database:**

Use PostgreSQL to create the necessary database:
```
\i file_path_to_database
```

5. Create a .env file:

Populate it with the following information. Ensure to change the database password to your actual database password:
```
DB_HOST=localhost
DB_PORT=port_number
DB_NAME=healthsync
DB_USER=postgres
DB_PASSWORD=your_db_password
```
## Usage
To run the program using the employee API:
```
python employee_api.py
```
To run the program using the patient API:
```
python patient_api.py
```
