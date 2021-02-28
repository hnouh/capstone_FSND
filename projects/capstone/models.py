import os
from sqlalchemy import Column, String, Integer, create_engine,DateTime,ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json 
from flask_migrate import Migrate
from flask import Flask

# ---------------------------------------------------------
# App Config.
# ---------------------------------------------------------
# database_host = os.getenv('DB_HOST', '127.0.0.1:5432')
# database_user = os.getenv('DB_USER', 'postgres')
# database_password = os.getenv('DB_PASSWORD', 'Ar648898')
# database_name = os.getenv('DB_NAME', 'CastingAgency')
database_path = 'postgres://naogqmhsxmzeuo:b7caf81f5e3c5629346356fc2f0e96c0ceb835acb306a45db94c86c26c0b5bff@ec2-54-220-35-19.eu-west-1.compute.amazonaws.com:5432/ddstbpre9t8qo0'
db = SQLAlchemy()   

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app 
    db.init_app(app) 

class Role(db.Model):
    __tablename__ = 'Role'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('Actor.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('Movie.id'), nullable=False)

'''
Actor
'''
class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    '''
  longActor()
      longActor form representation of the Actor model
  '''

    def longActor(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

'''
Movie
'''
class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    releaseDate = Column(DateTime())

    '''
  longMovie()
      longMovie form representation of the Movie model
  '''

    def longMovie(self):
        return {
            'id': self.id,
            'title': self.title,
            'releaseDate': self.releaseDate
        }

    def __init__(self, title, releaseDate):
        self.title = title
        self.releaseDate = releaseDate

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()