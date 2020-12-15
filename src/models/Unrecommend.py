from main import db
from models.Content import Content


class Unrecommend(db.Model):
    __tablename__ = "unrecommend"
    profile_id = db.Column(
        db.Integer, db.ForeignKey('profiles.profile_id'), primary_key=True)
    content_id = db.Column(
        db.Integer, db.ForeignKey('content.content_id'), primary_key=True)
    content = db.relationship(
        Content, back_populates="profiles", cascade="all, delete")
