# Introduction
## Objective
The objective of this project is to implement a data access and application layer for the additional features outlined in R7 and R8 of T3A2. Below is a summary on the fulfillment of each requirement code as specified in project brief.

**R1:** In summary of the suggestions in R7 and R8 specified in T3A2, it is to implement an two additional features for the Netflix platform namely:-
1. A groups feature where users can create, update, join and unjoin group and share watching content through those groups
2. The unrecommend functionality where individual profile owners can remove content from being recommended to them which will serve to improve on the recommendations algorithms for Netflix through machine learning.

**R2:** [Report 1: Privacy and Security Analysis](docs/report-privacy_security.md)

**R3:**[Report 2: Professional, Ethical and Legal Obligations](docs/report-prof_ethical_legal)

**R4, R9:** A data model is implemented on a PostgreSQL database with one-to-one, one-to-many and many-to-many relationships. The application interfaces with the database through the use of Object Relational Mapping (ORM) with SQLAlchemy. SQLAlchemy Marshmallow schemas are used to serialise, deserialise and validate data to and from the database and application for the view component. Below is the database entity diagram that has been implemented in this application.

![db-schema](docs/erd.png)

Database tables are created through ORM [models](src/models) and serialised through Marshmallow [schemas](src/schemas)

![ORM models](docs/ORM_model.png)
![schema-validation](docs/schema_validation.png). 

Integrity checks are performed on the controllers to check if users/admin are authorised to access functionalities within the application. Authentication and Authorisation are performed on both the API and web interfaces. 

![Integrity checks](docs/Integrity_checks.png)

**R5, R12:** The implementation of the features described in R1 is achieved through the use of the Flask framework in the MVC (Model-View-Controller) pattern. The file structure within the src folder is in accordance to the MVC pattern and described in further detail in the 'File Structure' section of this document. Evidence of the implementation of CRUD functions and data export can be found in [src/controllers](src/controllers) and further documented in the API and web application endpoint documentation below:

1.  API endpoints

    * [Raw format](docs/api_endpoints.yaml)
    * [swagger viewer](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/ashley190/T3A3/main/docs/api_endpoints.yaml)

2. Web application endpoints

    * [Raw format](docs/web_endpoints.yaml)
    * [Swagger viewer](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/ashley190/T3A3/main/docs/web_endpoints.yaml)

    Here is a full list of functionalities implemented in both the API and web interfaces (unless otherwise specified)

    ### Users
    * User registration
    * User login
    * User logout(web only)
    * View user/account info
    * Update user/account info
    * Delete user account

    ### Profiles
    * Show user profiles
    * Show individual profiles by id
    * Create new user profile
    * Update user profile
    * Delete user profile
    * Show available content for each profile(web only)
    * Show unrecommended content for each profile
    * Unrecommend content
    * Remove unrecommended content

    ### Groups
    * View all groups for all profiles
    * View group by id for group members and group admin
    * Create group - users who create group automatically becomes group admin
    * Update group for group admin only
    * Delete group for group admin only
    * Join group for all profiles
    * Unjoin group for group members
    * Remove member for group admin only
    * Add group content for group members
    * Remove group content for group members

    ### Content
    * Show all available content(API only)

    ### Admin
    Admin users are generated through the flask db-custom seed command and cannot be created any other way. Databases must be seeded for the admin function to be available.
    * Admin login
    * View user aggregate data
    * View group aggregate data
    * View content aggregate data - unrecommended and group content data
    * Create content
    * Delete content
    * Backup database
    * View available database backups
    * Restore database from selected backup


**R6:** There are two user interfaces implemented.

### API
* Access: Using an API Client such as Insomnia

* Endpoints are constructed according to the RESTful convention. Here are the endpoint documentation for the API:
    * [Raw format](docs/api_endpoints.yaml)
    * [swagger viewer](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/ashley190/T3A3/main/docs/api_endpoints.yaml)

* **Authentication and authorization**: API authentication uses JWT token and requires the token to be included in the header for endpoints that require authorization. 

    * Token is obtained through submitting the correct user/admin credentials to the login endpoints.
    ![token](docs/jwt_token.png) 
    * Authorization headers are constructed and sent for endpoints that require authorization.
    ![authorization headers](docs/auth_header.png)

* **Body**: Endpoints that require a body to be sent will accept it in a JSON format.
![Body](docs/json_body.png)

* **Responses**: Responses will also be received in a JSON format.
![Response](docs/json_response.png)

* Data validation and Error messages: Data is validated through the ORM and Marshmallow schemas and error messages are sent back to the user in the response data.
![Error messages](docs/APIerror.png)


### Web application
* Access: Using a web browser

* Endpoints for the web interface does not subscribe to the RESTful convention due to the restrictions on methods such as PUT, PATCH and DELETE on web browsers. Here are the endpoint documentation:
    * [Raw format](docs/web_endpoints.yaml)
    * [Swagger viewer](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/ashley190/T3A3/main/docs/web_endpoints.yaml)

* **Authentication and authorization**: Web authentication and authorisation is managed through the use of cookies through flask-login to maintain a Stateful session for a logged in user. Users/admin login through the login endpoint and if successful will gain access to user/admin functions.

![web login](docs/web_login.png)

* **Data display**: Data on the web application is typically displayed in a tabular format with options displayed as tables/links. All links are functional.

![web data](docs/web_data.png)

* **Create and Update functions**: Data is obtained for create and update functions through the use of forms.

![web form](docs/web_form.png)

* **Alerts**: Alert messages are available to inform users of errors and actions performed.

![alert](docs/alert.png)

**R7, R10, R11:** API and web endpoints that uses queries that aggregates and parse data can be found in both the [admin_controller](src/controllers/admin_controller.py) and [web_admin_controller](src/controllers/web_admin_controller.py). Both SQL and ORM queries are available with ORM queries being implemented and SQL queries commented out for reference.

![Code - Aggregating data](docs/data-aggregate-code.png)

**R8** Validation of user input is implemented through the use of Marshmallow schemas (example below). 
![schema_validation](docs/schema_validation.png)

Error messages will be displayed to the user on both the APi and web interface through different mechanisms:-
1. API - Custom error messages returned in the response data.
![API_error](docs/APIerror.png)

2. Web - Alert messages displayed on the browser
![Web_error](docs/alert.png)

# File structure
* [README.md](README.md) - This document
* [docs](docs) - contains all links and figures included in this README.
* [requirements.txt](requirements.txt) - application dependencies that needs to be installed for the application to be functional. See Installation section for details.
* [src](src) - source code for this application. Code is organised into several directories within src. This application is structured according to the MVC (Model-View-Controller) pattern.
    * [main.py](src/main.py) - main flask application. Registration and initiation of flask application.
    * [default_settings.py](src/default_settings.py) - Application configuration for different environments
    * [commands.py](src/commands.py) - custom commands that can be accessed on the command line interface. 
    * [.env.example](src/.env.example) - example .env file containing environment variables that need to be populated during the setup process 
    * [migrations](src/migrations) - database migration files to update database to the latest state as required by the application
    * [controllers](src/controllers) - route definition, request handling and application logic for API and web application endpoints. Web application controllers have the 'web_' prefix.
    * [models](src/models) - SQLAlchemy ORM models that interacts with the connected database.
    * [schemas](src/schemas) - SQLAlchemy Marshmallow schemas for serialisaton and deserialisation of database and python data
    * [templates](src/templates) - Jinja2 templates for rendering through the web application routes.
    * [forms.py](src/forms.py) - Forms constructed using wtforms for generating forms for the web interface, processed through web_controllers and rendered in the appropriate templates.
    * [tests](src/tests) - Integration tests for the API endpoints for use with Python's unittests
    * [backup](src/backup) - This does not come prepackaged in the application upon first clone but will be generated as the backup routes are used for backing up the database. Backups files are stored within timestamped folders and in separate files for separate database tables.


# Installation 
## Project folder and environment setup
The commands below assumes the use of bash script in a linux OS/mac OS. 
1. Install Python3.8, python3.8-venv and python3-pip installed on system

    `sudo apt-get install python3.8, python3.8-venv, python3-pip`

2. Obtain and navigate to project folder. This can be done through unzipping the project folder (as submitted) or cloning from github.

    `git clone https://github.com/ashley190/T3A3.git`

3. Create and activate virtual environment

    `python3.8 -m venv venv`
    `source venv/bin/activate`

4. Install requirements

    `pip install -r requirements.txt`


## Set up database

1. Install postgresql on your intended database host

    `sudo apt-get install postgresql`

2. Log into postgresql as postgres user

    `sudo -u postgres psql`

3. Set up 'netflix' database

    `CREATE DATABASE netflix;`

4. Create user 'flask'

    `CREATE ROLE flask;`

5. Grant all privileges on the 'netflix' database to 'flask'

    `GRANT ALL PRIVILEGES ON DATABASE netflix TO flask;`

6. Create password for the user 'flask' and enable user 'flask to login

    `ALTER USER flask WITH ENCRYPTED PASSWORD '<PASSWORD>';`

    `ALTER USER flask WITH LOGIN;`

7. Create the .env file within the src folder using the .env.example template and fill in the missing fields in the .env file:- If you've followed steps 3 - 6, the following fields should be:-

    * `<user>` = flask
    * `<password>` = password that was set for user flask
    * `<host>` = localhost or the public ip address where the postgres database is hosted
    * `<port>` = default port for postgresql is 5432
    * `<dbname>` = netflix

8. Set up other variables within the .env folder. These secret keys can be anything you specify but cannot be left blank.

9. Navigate to the src folder in the project and export the required flask environment variables. For example to load flask in the development environment, you can run the following commands in bash to export the required environment variables. The 'development' environment can be used to access both applications (recommended). These variables can also be included in the .env file for ease of future loading.

    `export FLASK_APP=main.py:create_app()`
    `export FLASK_ENV=development`

## Run Migrations
1. Initialise the use of migrations(not usually required)

    `flask db init`

2. Run all saved migrations

    `flask db upgrade`

3. Database tables can be seeded using the following command to populate with dummy data. Database tables MUST be seeded in order for admin functionality to be accessed:

    `flask db-custom seed`

    User and admin seed login data can be found in [commands.py](src/commands.py).

4. (Optional)To refresh the database, database tables can be dropped before running steps 2 and 3(optional) again or the database can be restored from a previous backup file. To drop the tables:

    `flask db-custom drop`

## Running automated tests
1. Scripts for automated tests are found in the [src/test/](src/tests) folder. The testing environment needs to be exported in order for the tests to run correctly. You'll also need to activate the python virtual environment and navigate into the src folder to run tests.

    `source venv/bin/activate`
    
    `cd src`

    `export FLASK_ENV=testing`

    `python -m unittest discover -s tests/ -v`

## Running the application on an AWS EC2 instance
1. If running the app on an EC2 instance, the EC2 instance must have be configured to accept incoming TCP connections on port 5000. This can be done through editing the inbound rules on the security group attached to the EC2 instance.

2. Activate the python virtual environment on the T3A3 folder and navigate to the src folder before running the flask app on your EC2 instance.

    (T3A3 folder) `source venv/bin/activate`

    `cd src`

    `python3 -m flask run -h 0.0.0.0`

3. Access the endpoints through the EC2 instance's public IP address. For example:

    `<EC2 public IP address>:5000/users/register`

**Note:** As the T3A3 folder on the EC2 instance will be deleted every time CI/CD is run, may be useful to store the .env file outside of the T3A3 folder and automate a copy of the .env file back into the T3A3/src location each time CI/CD is run. This has been included in line 45 of the ci-cd.yml file and must be excluded when doing the first deployment.





## Backup and Restore data through the command line
1. (Optional) If there are any saved postgresql pg_dump files, they can be restored using the following command.

    `pg_restore -h <host> -p <port> -d netflix -U flask -a <relative_file_path>`

2. In order to create a data dump on your current database, the following command can be used:

    `pg_dump -Fc -h <host> -U flask netflix -a > <relative_file_path/file_name>`

# Troubleshooting

1.  Cannot connect to database remotely(assuming a postgresql database is used)

    * Try running the following command:

    `psql --host=[Endpoint] --port=5432 --username=[username] --password --dbname=[database name]`

    * Try configuring the database config file:

        1. (in psql on the computer where your database resides) Run `show config_file` and `show hba_file` and note down both paths
        2. Exit psql and access config file through the path shown through `show config_file` in step 1.
        3. Under 'Connections and Authentication", unhash listen_addresses and change listen addresses='*'.
        4. Access the hba file through the path hown through `show hba_file` in step 1.
        5. Configure your hba_file settings to the following:-
        ![hba settings](docs/hba_settings.png)

2.  Web pages not loading correctly - try clearing the cache on your browser

3.  Can't login to admin interface - Run `flask db-custom seed` to ensure admin tables are seeded. Two admin users are created with the usernames 'Admin1' and 'Admin2' with password '654321'.

4. Backup function does not work on AWS EC2 flask application - Create the src/backup folder and change the owner of the folder to 'ubuntu'

    (in src folder)`mkdir backup`

    `sudo chown ubuntu backup`

5. (BUG) A known bug for AWS EC2 deployment - As the code for the download of database data on the admin endpoints only downloads to a predefined location in the code, the local folder and directories will be generated in a 'backup' directory and stored within the src folder of the project on the EC2 instance. This will interfere with future CI/CD deployments unless manually moved from its original location prior to running the CI/CD workflow and restored to the src folder once CI/CD is completed. This is due to the fact that the 'github-actions' user (CI/CD) will not have the privilege to remove that folder generated by the 'ubuntu' (application) user. Future fixes will include allowing users to specify their preferred location for backups and restore files.

# Continuous integration/Continuous Deployment(CI/CD)

**Continuous Integration(CI)**

The steps involved in the Continuous Integration(CI) workflow upon pushing onto GitHub:-
1. Checks out project from github into a virtual machine(VM) running on ubuntu-latest.
2. Installs Python3.8 on the VM
3. Installs dependencies as specified on requirements.txt
4. Run Automated tests
5. Checks code according to PEP8 style guide using flake8

**Continuous Deployment(CD)**

Upon successful completion of the CI process highlighted above, the code will then be deployed to an AWS EC2 instance set up for the code. GitHub Actions will connect to the EC2 instance via SSH and does a fresh install of the application and its dependencies on the AWS EC2 instance. In order to test this, you will need the following:-

1. Your own EC2 instance running on Ubuntu18.06 or later with python3.8, python3.8-venv and python3-pip installed.
2. A github-actions user set up on the EC2 instance
3. Generate an SSH key pair, store the public key under /home/github-actions/.ssh/authorized_keys and copy the private key into the secrets settings within your GitHub repo for T3A3 and name it SSH_KEY.
4. Obtain the public IP address from your EC2 instance and update the host field with the IP address of your EC2 instance on the [ci-cd.yml](.github/workflows/ci-cd.yml) file.
5. Run the CI/CD workflow and the application will now be installed and ready to run in a python virtual environment in /home/github-actions/T3A3.

**Note:** Running CI/CD will complete all the steps within 'Project folder and environment setup' in the 'Installation' section on your EC2 instance. 
To complete setting up the application, complete the steps listed under 'Set up database' and 'Run Migrations' for the app to be fully functional. These steps only need to be done once per instance. See Step 4 in 'Set up database' for options to refresh the database tables.

# User Guide

## API
Interaction with the API can be achieved through the use of an API client such as [Insomnia Core](https://insomnia.rest/download/). All steps below are demonstrated using Insomnia Core.

1. Using Insomnia Core - Insomnia core is a straightforward API client that can be used to interact with the API. For guidance on how to use Insomnia core, refer to their [official documentation](https://support.insomnia.rest/category/9-getting-started)

2. Refer to the [API endpoint documentation](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/ashley190/T3A3/main/docs/api_endpoints.yaml) for requirements for all the API endpoints. In summary, all request body and responses are sent and received in JSON format. Apart from the login and registration endpoints, all other endpoints will require a JWT token (generated at login) included in the header in the following format.
![Authorisation header](docs/auth_header.png)

## Web Interface
Interaction with the web interface requires a browser(preferably Google Chrome). Users are allowed to register for an account and login through the specified web endpoints to access the application. Here are some screenshots of the web application.

1. User Registration
![User Registration](docs/user_registration.png)

2. User Login
![User Login](docs/user_registration.png)

3. Profiles page with functional links to view, create, update and delete user profiles.
![Profiles](docs/Profiles.png)

4. Account info page with functional links to update and delete account.
![Account info](docs/Acc_info.png)

5. View individual profile page with content and unrecommended list as well as functional links to unrecommend and remove unrecommended contents. This page will have an additional navigation link to groups as they are linked to individual profiles.
![Profilebyid](docs/Profile_by_id.png)
![unrecommended](docs/unrecommend.png)

6. Group page - View all groups and functional links and buttons to view, join and unjoin groups for non-group administrators and view, edit and delete groups for group administrators. There is also a create group link for group creation. Group creators will be assigned the group admin by default.
![groups](docs/groups.png)

7. Admin login - login page for admin users
![admin login](docs/admin_login.png)

8. Admin users view - For admin users to view aggregate user data.
![admin users](docs/admin_users.png)

9. Admin groups view - For admin users to view aggregate group data.
![admin groups](docs/admin_groups.png)

10. Contents - For admin users to view, create and delete content.
![admin content](docs/admin_content.png)

11. Database backups - For admin users to view create and restore from database backup files.
![admin backup](docs/db_backups.png)
