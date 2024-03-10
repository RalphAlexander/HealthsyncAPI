## Set up this project locally
1. Clone the repo
```
git clone https://github.com/RalphAlexander/HealthsyncAPI
```
2. Install dotenv and psycopg2
```
pip install python-dotenv
pip install psycopg2
```
3. Create the database using postgres
```
\i file_path_to_database
```

4. Create a .env file with the following information. Don't forgot to change the password to ur db password and none of these are encased with ""
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=healthsync
DB_USER=postgres
DB_PASSWORD=your_db_password
```
5. Run the program using the command line
