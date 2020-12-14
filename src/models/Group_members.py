from main import db
from models.Group import Group


class GroupMembers(db.Model):
    __tablename__ = "group_members"
    profile_id = db.Column(
        db.Integer, db.ForeignKey('profiles.profile_id'), primary_key=True)
    group_id = db.Column(
        db.Integer, db.ForeignKey('groups.group_id'), primary_key=True)
    admin = db.Column(db.Boolean)
    groups = db.relationship(Group, back_populates="profiles")
