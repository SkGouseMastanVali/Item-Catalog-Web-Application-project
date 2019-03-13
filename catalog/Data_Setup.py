import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class GmailUser(Base):
    __tablename__ = 'gmailuser'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(220), nullable=False)


class BagCompanyName(Base):
    __tablename__ = 'bagcompanyname'
    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    user_id = Column(Integer, ForeignKey('gmailuser.id'))
    user = relationship(GmailUser, backref="bagcompanyname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class BagName(Base):
    __tablename__ = 'bagname1'
    id = Column(Integer, primary_key=True)
    bagname = Column(String(350), nullable=False)
    color = Column(String(150))
    rating = Column(String(150))
    bagtype = Column(String(150))
    price = Column(String(10))
    date = Column(DateTime, nullable=False)
    bagcompanynameid = Column(Integer, ForeignKey('bagcompanyname.id'))
    bagcompanyname = relationship(
        BagCompanyName, backref=backref('bagname1', cascade='all, delete'))
    gmailuser_id = Column(Integer, ForeignKey('gmailuser.id'))
    gmailuser = relationship(GmailUser, backref="bagname1")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'bagname': self. bagname,
            'color': self. color,
            'rating': self. rating,
            'price': self. price,
            'bagtype': self. bagtype,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///bags.db')
Base.metadata.create_all(engin)
