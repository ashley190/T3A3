from main import db
from models.Group_members import GroupMembers
from models.Content import Content
from models.joined_tables import unrecommend


class Profile(db.Model):
    __tablename__ = "profiles"

    profile_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    restrictions = db.Column(db.String(), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    groups = db.relationship(GroupMembers, cascade="all, delete")
    unrecommend = db.relationship(
        Content, secondary=unrecommend, lazy="subquery",
        backref=db.backref('profile', lazy=True), cascade="all, delete")

    def __repr__(self):
        return f"<Profile {self.profile_id}>"
