from sqlalchemy import Column, Integer, String, Float, Boolean, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Wstatus(Base):
    __tablename__ = 'wstatus'
    id = Column(Integer, primary_key=True)
    level = Column(String, nullable=False, default="w")
    chatId = Column(Integer, unique=True)


engine = create_engine('sqlite:///bdconectate.db')
# Initalize the database if it is not already.
Base.metadata.create_all(engine)

# Create a session to handle updates.
Session = sessionmaker(bind=engine)
session = Session()


