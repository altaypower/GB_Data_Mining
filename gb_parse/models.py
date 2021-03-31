
import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Boolean


Base = declarative_base()

class InstaUser(Base):
    __tablename__ = "instauser"
    date_parse = Column(DateTime, nullable=False)
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)

class InstaFollow(Base):
    __tablename__ = "instafollow"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("instauser.user_id"))
    user_name = Column(String, nullable=False)
    follow_id = Column(Integer, ForeignKey("instauser.user_id"))
    follow_name = Column(String, nullable=False)
    instauser = relationship("InstaUser")

class InstaFollowed(Base):
    __tablename__ = "instafollowed"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("instauser.user_id"))
    user_name = Column(String, nullable=False)
    followed_id = Column(Integer, ForeignKey("instauser.user_id"))
    followed_name = Column(String, nullable=False)
    instauser = relationship("InstaUser")
