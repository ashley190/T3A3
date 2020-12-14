from main import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    subscription_status = db.Column(db.Boolean)
    profiles = db.relationship(
        "Profile", backref="user", lazy="dynamic",
        cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
