from main import db


class Group(db.Model):
    __tablename__ = "groups"

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    Description = db.Column(db.String())

    def __repr__(self):
        return f"<Group {self.group_id}>"
