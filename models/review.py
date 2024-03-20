#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review class to store review information """
    __tablename__ = "reviews"
    if models.storage_type == 'db':
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id',
                          ondelete="CASCADE"), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id',
                         ondelete="CASCADE"), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""
