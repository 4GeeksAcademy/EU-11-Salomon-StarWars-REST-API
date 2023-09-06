import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref, declarative_base, sessionmaker
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

engine = create_engine('sqlite:///starwars.db')
Session = sessionmaker(bind=engine)
session = Session()

user_favorites_table = Table('user_favorites', Base.metadata,
                             Column('user_id', Integer, ForeignKey('users.id')),
                             Column('favorite_id', Integer, ForeignKey('favorites.id')))

class User(Base):
    __tablename__ = 'users'
    # To define columns for the table person
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)

    favorites = relationship("Favorite", 
                             secondary=user_favorites_table,
                             back_populates="users")

class Account(Base):
    __tablename__ = 'accounts'
    # This define columns for the table address.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    username= relationship(User)
    address = Column (String(250))          


class Favorite(Base):
    __tablename__ = 'favorites'
    # Here we define columns for the table person
    type = Column(String)
    id = Column(Integer, primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'favorite',
        'polymorphic_on': type
    }

    users = relationship("User", 
                         secondary=user_favorites_table,
                         back_populates="favorites")

class Character(Favorite):
    __tablename__ = 'characters'
    id = Column(Integer, ForeignKey('favorites.id'), primary_key=True)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'character',
    }

class Planet(Favorite):
    __tablename__ = 'planets'
    id = Column(Integer, ForeignKey('favorites.id'), primary_key=True)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'planet',
    }

class Vehicle(Favorite):
    __tablename__ = 'vehicles'
    id = Column(Integer, ForeignKey('favorites.id'), primary_key=True)
    name = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'vehicle',
    }

class CharacterPeople(Character): 
    __tablename__ = 'people'
    id = Column(Integer, ForeignKey('characters.id'), primary_key=True)
    name = Column(String)

    def to_dict(self):
        return {}

# Draw from SQLAlchemy base
render_er(Base, 'diagram.png')

Base.metadata.create_all(engine)


# Create a new user
new_user = User(name="Anakin Skywalker", email="anakinskywalker@gmail.com")

session.add(new_user)

fav_character = Character(name="Grogu")
fav_planet = Planet(name="Alderaan")
fav_vehicle = Vehicle(name="A-wing fighter")

new_user.favorites.extend([fav_character, fav_planet, fav_vehicle])

session.commit()