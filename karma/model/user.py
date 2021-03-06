from sqlalchemy.orm import relationship
from karma.database import db
from karma.model.job import Job
from karma.model.award import Award
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    jobs = relationship('Job', back_populates="user")
    awards = relationship('Award', back_populates="user")
    name = db.Column(db.String(250), nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, name, password, is_admin=False):
        self.name = name
        self.password = password
        self.id = None
        self.is_admin = is_admin

    def add(self, thing):
        if isinstance(thing, Job):
            self.jobs.append(thing)
        elif isinstance(thing, Award):
            self.awards.append(thing)
        else:
            raise Exception

    @property
    def score(self):
        return len(self.jobs)-len(self.awards)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        pass

    def is_active(self):
        # Return false is inactivated or rejected
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return f'User ({self.name})'

    def __repr__(self):
        return str(self)
