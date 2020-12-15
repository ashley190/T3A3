from main import db
from models.Content import Content


class GroupContent(db.Model):
    __tablename__ = "group_content",
    group_id = db.Column(db.Integer, db.ForeignKey(
        'groups.group_id', ondelete='CASCADE'), primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey(
        'content.content_id', ondelete='CASCADE'), primary_key=True)
    content = db.relationship(
        Content, back_populates="groups", cascade="all, delete")
