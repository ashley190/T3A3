# Introduction
**Objective**: The objective of this project is to implement a data access and application layer for the additional features outlined in R7 and R8 of T3A2. Below is the proposed database schema to be implemented.

![db-schema](docs/erd.png)

**Functionality**:
There are two user interfaces that can be accessed using separate methods and has the following functionality:

1. API: Using an API Client such as Insomnia

    Endpoints are constructed according to the RESTful convention and its raw format can be viewed [here](docs/api_endpoints.yaml). This can also be displayed using the [swagger viewer](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/ashley190/T3A3/main/docs/api_endpoints.yaml).2. Web_app: Using a web browser

2. Web application: Using a web browser

    

# File structure

# Installation 
The commands below assumes the use of bash script in a linux OS/mac OS. 
1. Install Python3.8, python3.8-venv and python3-pip installed on system

    `sudo apt-get install python3.8, python3.8-venv, python3-pip`

2. Git clone and navigate to project folder

    `git clone <https link on github>`

3. Create and activate virtual environment

    `python3.8 -m venv venv`
    `source venv/bin/activate`

4. Install requirements

    `pip install -r requirements.txt`


## Set up database

1. Install postgresql on your intended database host
2. Log into postgresql as postgres user
3. Set up 'netflix' database

    `CREATE DATABASE netflix;`

4. Create user 'flask'

    `CREATE ROLE flask;`

5. Grant all privileges on the 'netflix' database to 'flask'

    `GRANT ALL PRIVILEGES ON DATABASE netflix TO flask;`

6. Create password for the user 'flask'

    `ALTER USER flask WITH ENCRYPTED PASSWORD '<PASSWORD>'`

7. Create the .env file using the .env.example template and fill in the missing fields in the .env file:- If you've followed steps 3 - 6, the following fields should be:-

    * `<user>` = flask
    * `<password>` = password that was set for user flask
    * `<host>` = localhost or the public ip address where the postgres database is hosted
    * `<port>` = default port for postgresql is 5432
    * `<dbname>` = netflix

8. Navigate to the src folder in the project and export the required flask environment variables. For example to load flask in the development environment, you can run the following commands in bash to export the required environment variables.

    `export FLASK_APP=main.py:create_app()`
    `export FLASK_ENV=development`

## Run Migrations and restore data
1. Initialise the use of migrations

    `flask db init`

2. Run all saved migrations

    `flask db upgrade`

3. (Optional) If there are any saved postgresql pg_dump files, they can be restored using the following command.

    `pg_restore -h <host> -p <port> -d netflix -U flask -a <relative_file_path>`

## Create database data dump
1. In order to create a data dump on your current database, the following command can be used:

    `pg_dump -Fc -h <host> -U flask netflix -a > <relative_file_path/file_name>`



# CI/CD
Continuous integration

The steps involved in the Continuous Integration(CI) workflow upon pushing onto GibHub:-
1. Checks out project from github into a virtual machine(VM) running on ubuntu-latest.
2. Installs Python3.8 on the VM
3. Installs dependencies as specified on requirements.txt
4. Run Automated tests
5. Checks code according to PEP8 style guide using flake8

# Report 1:

# Report 2:

Passwords hashed
Input validation at schema and model level
Error handling upon incorrect input
Password hash not returned during schema serialisation
Use token authentication (expiry 1 day)
Token generation process using JWT where secret key is stored and retrieved from environment variables during production(diff from development key)
User authorisation implemented to perform CRUD actions on user owned profiles only
Separate logins to admin interface (separate endpoints)
Require business end to manage admin accounts - account creation, deletion and further segregation of responsibilities within admin accounts if possible considering security factors.
