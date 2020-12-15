from main import db
from models.Group_content import GroupContent
from models.Unrecommend import Unrecommend


class Content(db.Model):
    __tablename__ = "content"

    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String())
    year = db.Column(db.Integer)
    groups = db.relationship(
        GroupContent, back_populates="content", cascade="all, delete")
    profiles = db.relationship(
        Unrecommend, back_populates="content", cascade="all, delete")

    def __repr__(self):
        return f"<Content {self.content_id}>"
