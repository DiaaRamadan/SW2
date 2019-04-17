from sqlalchemy import (Column,
                        String,
                        Integer,
                        create_engine,
                        ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

engine = create_engine('sqlite:///database.db')


class user(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # company type 2 and normal user is 1
    type = Column(String)

    @property
    def serilize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,

            'type': self.type
        }

class intersted(Base):
    __tablename__ = 'interested'
    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    interested = Column(Integer, nullable=False)
    skills = Column(String)

    user_id = Column(Integer, ForeignKey('User.id'))
    users = relationship(user)

    @property
    def serilize(self):
        return {
            'id': self.id,
            'interested': self.interested,
            'filed': self.skills,
        }


class quiz(Base):
    __tablename__ = 'quizs'
    id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    description = Column(String, nullable=False)
    field = Column(String, nullable=False)

    @property
    def serilize(self):
        return {
            'id': self.id,
            'description': self.description,
            'filed': self.field,
        }

engin = create_engine('sqlite:///database.db')
Base.metadata.create_all(engin)