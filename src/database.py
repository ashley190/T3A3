import psycopg2
import os


connection = psycopg2.connect(
    database="netflix",
    user="flask",
    password=os.getenv("DB_PW"),
    host="54.196.130.96",
    port="5432"
)

cursor = connection.cursor()

cursor.execute("create table if not exists profiles (profile_id serial PRIMARY KEY, name varchar, restrictions varchar);")  # noqa: E501
connection.commit()
