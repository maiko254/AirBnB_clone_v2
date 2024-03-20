#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity

place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60), ForeignKey('places.id',
                             onupdate="CASCADE", ondelete="CASCADE"),
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey('amenities.id', onupdate="CASCADE",
                                        ondelete="CASCADE"), nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if models.storage_type == 'db':
        city_id = Column(String(60), ForeignKey('cities.id',
                         ondelete="CASCADE"), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id',
                         ondelete="CASCADE"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", cascade="all, delete",
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False, overlaps="place_amenities")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """ """
            review_list = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """ """
            amenity_list = []
            amenity_dict = models.storage.all(Amenity)
            for k, v in amenity_dict.items():
                for amenity_id in amenity_ids:
                    key = Amenity.__name__ + '.' + amenity_id
                    if k == key:
                        amenity_list.append(v)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """ """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
