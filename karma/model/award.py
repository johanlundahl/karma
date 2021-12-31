from datatime import datetime
from sqlalchemy.orm import relationship
from karma.database import db


class Award(db.Model):

    __tablename__ = 'awards'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    user = relationship('User', back_populates='awards')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self):
        self.created = datetime.now()

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f'Award (for {self.user.name})'

    def __repr__(self):
        return str(self)
