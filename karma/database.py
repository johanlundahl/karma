from flask_sqlalchemy import SQLAlchemy, BaseQuery


class Db(SQLAlchemy):

    def create(self):
        self.create_all()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.commit()

    def add(self, item):
        self.session.add(item)
        return item

    def delete(self, item):
        self.session.delete(item)

    def all(self, type):
        return self.session.query(type).all()

    def get(self, type):
        return Query(self.session.query(type), type)


db = Db()


class Query(BaseQuery):

    def __init__(self, query, type):
        self.query = query
        self.type = type

    def where(self, name, value):
        self.query = self.query.filter(name == value)
        return self

    def all(self):
        return self.query.all()

    def one(self):
        return self.query.first()

    def first(self):
        return self.query.first()
