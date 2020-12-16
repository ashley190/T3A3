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
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted!")


@db_commands.cli.command("seed")
def seed_db():
    from models.Profile import Profile
    from models.User import User
    from models.Group import Group
    from models.Content import Content
    from models.Group_members import GroupMembers
    from main import bcrypt
    import random
    from faker import Faker

    faker = Faker()
    users = []
    contents = []

    for i in range(1, 6):
        user = User()
        user.email = f"test{i}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        user.subscription_status = random.choice([0, 1])
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print("User table seeded")

    for i in range(30):
        content = Content()
        content.title = faker.sentence()
        content.genre = faker.word()
        content.year = faker.year()
        db.session.add(content)
        contents.append(content)

    db.session.commit()
    print("Content table seeded")

    for i in range(10):
        content = random.sample(contents, k=2)
        restrictions = ("G", "PG", "M", "MA15+", "R18+")
        profile = Profile()
        profile.name = faker.first_name_nonbinary()
        profile.restrictions = random.choice(restrictions)
        profile.user_id = random.choice(users).user_id
        profile.unrecommend.extend(content)
        db.session.add(profile)

    db.session.commit()
    print("Profile table seeded")

    for i in range(10):
        content = random.sample(contents, k=3)
        group = Group()
        group.name = faker.word()
        group.description = faker.text()
        group.content.extend(content)
        GroupMembers(
            groups=group, profile_id=random.randrange(1, 11),
            admin=random.choice([0, 1]))
        db.session.add(group)

    db.session.commit()
    print("Group table seeded")
