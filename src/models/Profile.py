from main import db
from models.Group_members import group_members
from models.Group import Group


class Profile(db.Model):
    __tablename__ = "profiles"

    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    restrictions = db.Column(db.String(), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    groups = db.relationship(
        Group, secondary=group_members, lazy="subquery", backref=db.backref(
            "profile", lazy=True))

    def __repr__(self):
        return f"<Profile {self.profile_id}>"
