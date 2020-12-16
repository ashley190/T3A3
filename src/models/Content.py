from main import db
from models.joined_tables import group_content, unrecommend


class Content(db.Model):
    __tablename__ = "content"

    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String())
    year = db.Column(db.Integer)
    groups = db.relationship(
        "Group", secondary=group_content, backref=db.backref("contents"))
    profiles = db.relationship(
        "Profile", secondary=unrecommend, backref=db.backref("contents"))

    def __repr__(self):
        return f"<Content {self.content_id}>"
