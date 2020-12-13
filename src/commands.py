from main import db
from flask import Blueprint

db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created!")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted!")


@db_commands.cli.command("seed")
def seed_db():
    from models.Profile import Profile
    import random
    from faker import Faker
    faker = Faker()

    for i in range(20):
        restrictions = ("G", "PG", "M", "MA15+", "R18+")
        profile = Profile()
        profile.name = faker.first_name_nonbinary()
        profile.restrictions = random.choice(restrictions)
        db.session.add(profile)

    db.session.commit()
    print("Tables seeded!")
