from main import db


class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"
