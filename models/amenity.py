#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class Amenity(BaseModel, Base):
    """ Defines class to store the amenities found in an AirBnB house """
    __tablename__ = "amenities"
    if models.storage_type == 'db':
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity")
    else:
        name = ""
