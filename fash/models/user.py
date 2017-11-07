from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///fash.db', echo=True)
Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'

    id              = Column(Integer, primary_key=True)
    email           = Column(String(255), nullable=False)
    name            = Column(String(255), nullable=False)
    family          = Column(Integer, ForeignKey('Families.id'))
    points          = Column(Integer)
    completed       = relationship('Completed', backref='player', lazy='dynamic')

class Tasks(Base):
    __tablename__ = 'Tasks'

    id              = Column(Integer, primary_key=True)
    name            = Column(String(255))
    value           = Column(Integer)
    active          = Column(Boolean)
    completed       = relationship('Completed', backref='task', lazy='dynamic')

class Families(Base):
    __tablename__ = 'Families'

    id              = Column(Integer, primary_key=True)
    name            = Column(String(255))
    member          = relationship('Users', backref='fam_mem', lazy='dynamic')

class Completed(Base):
    __tablename__ = 'Completed'

    id              = Column(Integer, primary_key=True)
    user            = Column(Integer, ForeignKey('Users.id'))
    task_name       = Column(Integer, ForeignKey('Tasks.id'))
    valid           = Column(Boolean)

Base.metadata.create_all(engine)
