from main import db


group_content = db.Table(
    'group_content',
    db.Column(
        'group_id', db.Integer, db.ForeignKey(
            'groups.group_id', ondelete='CASCADE'), primary_key=True),
    db.Column(
        'content_id', db.Integer, db.ForeignKey(
            'content.content_id', ondelete='CASCADE'), primary_key=True))

unrecommend = db.Table(
    'unrecommend',
    db.Column(
        'profile_id', db.Integer, db.ForeignKey(
            'profiles.profile_id', ondelete='CASCADE'), primary_key=True),
    db.Column(
        'content_id', db.Integer, db.ForeignKey(
            'content.content_id', ondelete='CASCADE'), primary_key=True))
