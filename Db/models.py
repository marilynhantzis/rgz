from . import db
from flask_login import UserMixin


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(30), nullable=False, unique=True )
    password =  db.Column(db.String(102), nullable=False)


class seans(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable=False, unique=True )
    time = db.Column(db.String(30), nullable=False)
    data = db.Column(db.Date, nullable=False)
    def __repr__(self):
        return f"id:{self.id}, title: {self.title}, time: {self.time}, data: {self.data}"


class reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    seans = db.Column(db.Integer, db.ForeignKey('seans.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    seat = db.Column(db.Integer)
    def __repr__(self):
        return f"id:{self.id}, seans: {self.seans}, user: {self.user}, seat: {self.seat}"