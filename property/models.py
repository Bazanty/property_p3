


from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    clients = relationship('Client', back_populates='agent')
    properties = relationship('Property', back_populates='agent')

class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    location = Column(String, nullable=False)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    agent = relationship('Agent', back_populates='properties')
    rooms = relationship('Room', back_populates='property')
    clients = relationship('Client', back_populates='property')

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    size = Column(Float, nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id'))
    property = relationship('Property', back_populates='rooms')

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    agent_id = Column(Integer, ForeignKey('agents.id'))
    agent = relationship('Agent', back_populates='clients')
    property_id = Column(Integer, ForeignKey('properties.id'))
    property = relationship('Property', back_populates='clients')
    payments = relationship('Payment', back_populates='client')

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='payments')
