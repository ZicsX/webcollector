# webscraper/models.py

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Sequence,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, Sequence("website_id_seq"), primary_key=True)
    domain = Column(String(255), unique=True, nullable=False)
    last_crawled = Column(DateTime, default=datetime.datetime.utcnow)

    webpages = relationship("WebPage", back_populates="website")


class WebPage(Base):
    __tablename__ = "webpages"

    id = Column(Integer, Sequence("webpage_id_seq"), primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False)
    url = Column(String(2000), nullable=False)
    file_name = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    website = relationship("Website", back_populates="webpages")


# Replace with your Oracle DB connection string
DATABASE_URL = "oracle+cx_oracle://username:password@localhost:1521/orcl"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
