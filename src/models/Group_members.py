from main import db

group_members = db.Table(
    "group_members",
    db.Column(
        "profile_id",
        db.Integer,
        db.ForeignKey("profiles.profile_id"), primary_key=True),
    db.Column(
        "group_id",
        db.Integer,
        db.ForeignKey("groups.group_id"), primary_key=True)
)
