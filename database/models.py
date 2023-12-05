from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    tg_id = Column(BigInteger, nullable=False)
    city = Column(String)
    reports = relationship('WeatherReport', backref='report', lazy=True, cascade='all, delete-orphan')
    #reviews = relationship('Reviews', backref='book', lazy=True)
    #readers = relationship('User', secondary=association_table, back_populates='books', lazy=True)
    
    def __repr__(self):
        return self.tg_id
    
class WeatherReport(Base):
    __tablename__ = 'WeatherReports'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('Users.id'), nullable=False)
    date = Column(DateTime, default=datetime.now, nullable=False)
    temp = Column(Integer, nullable=False)
    feels_like = Column(Integer, nullable=False)
    wind_speed = Column(Integer, nullable=False)
    pressure_nm = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    #book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    #user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return self.city
    
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()