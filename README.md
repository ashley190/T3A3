# Introduction
**Objective**: The objective of this project is to implement a data access and application layer for the additional features outlined in R7 and R8 of T3A2. Below is the proposed database schema to be implemented.

![db-schema](docs/erd.png)

# CI/CD
Continuous integration

The steps involved in the Continuous Integration(CI) workflow upon pushing onto GibHub:-
1. Checks out project from github into a virtual machine(VM) running on ubuntu-latest.
2. Installs Python3.8 on the VM
3. Installs dependencies as specified on requirements.txt
4. Run Automated tests
5. Checks code according to PEP8 style guide using flake8

# File structure

# Installation
Install Python3.8, python3.8-venv and python3-pip installed on system
Git clone and navigate to folder
Activate virtual environment
Install requirements
Set up .env


# Endpoints:
Endpoints are constructed according to the RESTful convention and its raw format can be viewed [here](docs/endpoints.yaml). This can also be displayed using the [swagger viewer](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/ashley190/T3A3/main/docs/endpoints.yaml).

# Report 1:

# Report 2:

Passwords hashed
Input validation at schema and model level
Error handling upon incorrect input
Password hash not returned during schema serialisation
Use token authentication (expiry 1 day)
Token generation process using JWT where secret key is stored and retrieved from environment variables during production(diff from development key)