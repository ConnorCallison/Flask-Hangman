from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'
	name = Column(String(15), nullable = True)
	wins = Column(Integer, primary_key = False)
	losses = Column(Integer, primary_key = False)
	id = Column(Integer, primary_key = True)

# End of file
engine = create_engine('sqlite:///scores.db')
Base.metadata.create_all(engine)