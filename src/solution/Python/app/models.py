import os
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_login import UserMixin
from datetime import timedelta

# safe imports
__all__ = ('Beer', 'Brewery', 'BeerPhotos', 'User', 'Category', 'Style', 'engine', 'Base', 'session')

# db path, make sure "check_same_thread" is set to False
thisDir = os.path.dirname(__file__)
db_path = os.path.join(os.path.dirname(thisDir), 'db').replace(os.sep, '/')

# make sure folder exists
if not os.path.exists(db_path):
    os.makedirs(db_path)

# VERY IMPORTANT - our connection string.  SqlAlchemy can work with many different database formats
# we are using sqlite for demo purposes (using multithreaded to prevent locks)
brewery_str = 'sqlite:///{}/beer.db?check_same_thread=False'.format(db_path) 

# get declaritive base context
Base = declarative_base()

# basic repr
def basic_repr(obj, attr):
    """ returns a basic representation of an object

    :param obj: table object
    :param attr: attribute used to label unique object
    """
    return '<{}: "{}">'.format(obj.__class__.__name__, getattr(obj, attr))


class BeerPhotos(Base):
    __tablename__ = 'beer_photos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    beer_id = Column(Integer, ForeignKey('beers.id'))
    photo_name = Column(String(100))
    data = Column(LargeBinary, default=None) #field is only used when config.photo_storage_type is 'database'

    def __repr__(self):
        return basic_repr(self, 'photo_name')


class Beer(Base):
    __tablename__ = 'beers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    brewery_id = Column(Integer, ForeignKey('breweries.id'))
    name = Column(String(150))
    description = Column(String(500), default=None)
    style = Column(String(50), default=None)
    alc = Column(Float, default=None)
    ibu = Column(Integer, default=None)
    color = Column(String(25), default=None)
    photos = relationship(BeerPhotos, cascade="all, delete-orphan")
    created_by = Column(Integer, ForeignKey('users.id'))
    brewery = relationship('Brewery', back_populates='beers')
    user = relationship('User', back_populates='submitted_beers')

    def __repr__(self):
        return '<{}: "{}" ({})>'.format(self.__class__.__name__, self.name, self.style)


class Brewery(Base):
    __tablename__ = 'breweries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    address = Column(String(100))
    city = Column(String(50))
    state = Column(String(2))
    zip = Column(String(11))
    monday = Column(String(30), default=None)
    tuesday = Column(String(30), default=None)
    wednesday = Column(String(30), default=None)
    thursday = Column(String(30), default=None)
    friday = Column(String(30), default=None)
    saturday = Column(String(30), default=None)
    sunday = Column(String(30), default=None)
    comments = Column(String(255), default=None)
    brew_type = Column(String(50), default='Brewery')
    website = Column(String(255), default=None)
    x = Column(Float)
    y = Column(Float)
    created_by = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='submitted_breweries')
    beers = relationship('Beer', back_populates='brewery', cascade="all, delete-orphan")

    def __repr__(self):
        return basic_repr(self, 'name')


class Style(Base):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_id = Column(Integer, ForeignKey('categories.id'))
    style_name = Column(String(100), nullable=False)
    last_mod = Column(DateTime, default=datetime.utcnow())
    category = relationship('Category', back_populates='styles')

    def __repr__(self):
        return basic_repr(self, 'style_name')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_name = Column(String(100), nullable=False)
    last_mod = Column(DateTime, default=datetime.utcnow())
    styles = relationship('Style', back_populates='category', cascade="all, delete-orphan")

    def __repr__(self):
        return basic_repr(self, 'cat_name')


# this must implement Flask-Login's UserMixin class to work with decorators!
class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String(64))
    created = Column(DateTime, default=datetime.utcnow())
    last_login = Column(DateTime)
    expires = Column(DateTime, default=datetime.utcnow() + timedelta(hours=8))
    activated = Column(String(5), default='False')
    submitted_breweries = relationship('Brewery')
    submitted_beers = relationship('Beer')

    @property
    def is_active(self):
        """ override UserMixin.is_active property """
        return self.activated == 'True'

    def __repr__(self):
        return basic_repr(self, 'username')

    def __str__(self):
        return repr(self)


# make sure all databases are created
engine = create_engine(brewery_str)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
