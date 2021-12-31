from enum import Enum
from datetime import datetime
from sqlalchemy.orm import relationship
from werkzeug.routing import BaseConverter
from karma.database import db


class JobType(Enum):

    DISHES = 'tömt diskmaskinen'
    VACUUM = 'damsugt'
    BREAKFAST = 'gjort frukost'

    @classmethod
    def parse(cls, key):
        return cls[key.upper()]

    def __str__(self):
        return self.name.lower()


class JobConverter(BaseConverter):

    def to_python(self, value):
        return JobType.parse(value)

    def to_url(self, values):
        return str(values)


class Job(db.Model):

    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    jobtype = db.Column(db.Enum(JobType))
    user = relationship('User', back_populates='jobs')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, type):
        self.jobtype = type
        self.created = datetime.now()

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def Dishes(self):
        return Job(JobType.DISHES)

    @classmethod
    def Vacuum(self):
        return Job(JobType.VACUUM)

    @classmethod
    def Breakfast(self):
        return Job(JobType.BREAKFAST)

    def __str__(self):
        return f'Job ({self.jobtype} for {self.user.name})'

    def __repr__(self):
        return str(self)
