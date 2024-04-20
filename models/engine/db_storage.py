#!/usr/bin/python3
""" Defines how to handle database storage in HBNB clone project """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """ Class that defines attributes and methods to handle database
    storage """
    __engine = None
    __session = None

    def __init__(self):
        """ handles initialization of DBStorage instance """
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, passwd, host, db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Return a dictionary of instances of cls or all objects
        if cls is None from the database """
        if cls:
            objs = self.__session.query(cls).all()
        else:
            us = self.__session.query(User).all()
            state = self.__session.query(State).all()
            city = self.__session.query(City).all()
            amenity = self.__session.query(Amenity).all()
            place = self.__session.query(Place).all()
            review = self.__session.query(Review).all()

            objs = us + state + city + amenity + place + review

        all_objs = {}
        for obj in objs:
            key = type(obj).__name__ + '.' + obj.id
            all_objs.update({key: obj})
        return all_objs

    def new(self, obj):
        """ Adds object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes obj from the database if obj is not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables in the database and creates the current
        database session from the engine """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))
        self.__session = Session

    def close(self):
        """ """
        self.__session.remove()
