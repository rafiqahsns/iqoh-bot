from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://sircpqrmnztntm:6b13289c884778c4252dccde30fc76fb64c87e337811b43851029380484fcb87@ec2-52-207-25-133.compute-1.amazonaws.com:5432/d8dt10qahvtjv7"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class birthdays(db.Model):
    __tablename__ = 'birthdays'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    birth_date = db.Column(db.DATE)

    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

class quotes(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text())

    def __init__(self, name, date):
        self.quote = quote

class notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text())

    def __init__(self, name, date):
        self.note = note

class events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    date = db.Column(db.DATE)

    def __init__(self, name, date):
        self.name = name
        self.date = date

if __name__ == '__main__':
    manager.run()


