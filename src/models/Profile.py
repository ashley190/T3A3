from main import db


class Profile(db.Model):
    __tablename__ = "profiles"

    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    restrictions = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Profile {self.profile_name}>"
