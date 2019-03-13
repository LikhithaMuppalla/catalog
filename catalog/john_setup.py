import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class emailUser(Base):
    __tablename__ = 'emailuser'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(205), nullable=False)


class BagCompanyName(Base):
    __tablename__ = 'bagcompanyname'
    id = Column(Integer, primary_key=True)
    name = Column(String(333), nullable=False)
    user_id = Column(Integer, ForeignKey('emailuser.id'))
    user = relationship(emailUser, backref="bagcompanyname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class BagName(Base):
    __tablename__ = 'bagname'
    id = Column(Integer, primary_key=True)
    itemname = Column(String(255), nullable=False)
    description = Column(String(555))
    price = Column(String(900))
    rating = Column(String(150))
    date = Column(DateTime, nullable=False)
    bagcompanynameid = Column(Integer, ForeignKey('bagcompanyname.id'))
    bagcompanyname = relationship(
        BagCompanyName, backref=backref('bagname', cascade='all, delete'))
    emailuser_id = Column(Integer, ForeignKey('emailuser.id'))
    emailuser = relationship(emailUser, backref="bagname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'itemname': self. itemname,
            'description': self. description,
            'price': self. price,
            'rating': self. rating,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///bags.db')
Base.metadata.create_all(engin)
