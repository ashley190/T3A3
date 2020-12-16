from main import db
from models.Content import Content
from models.joined_tables import group_content


class Group(db.Model):
    __tablename__ = "groups"

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    profiles = db.relationship("GroupMembers", back_populates="groups")
    content = db.relationship(
        Content, secondary=group_content, lazy="subquery",
        backref=db.backref('group', lazy=True), cascade="all, delete")

    def __repr__(self):
        return f"<Group {self.group_id}>"
