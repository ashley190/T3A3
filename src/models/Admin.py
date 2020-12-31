from main import db, bcrypt
from flask_login import UserMixin


class Admin(UserMixin, db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self):
        try:
            return str(self.admin_id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __repr__(self):
        return f"<Admin {self.username}>"
