# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#from pymongo import MongoClient
from scrapy import Request
#from scrapy.pipelines.images import ImagesPipeline
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import Session
import os
from scrapy.exceptions import DropItem

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Boolean
from . items import InstaUserItem, InstaFollowItem, InstaFollowedItem


class GbParsePipeline:
    def process_item(self, item, spider):
        return item

Base = declarative_base()

class InstaUser(Base):
    __tablename__ = "instauser"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_parse = Column(DateTime, nullable=False)
    user_id = Column(Integer, unique=True)
    user_name = Column(String, nullable=False)
    depth = Column(Integer)

    def __init__(self, date_parse, user_id, user_name, depth):
        self.date_parse = date_parse
        self.user_id = user_id
        self.user_name = user_name
        self.depth = depth

    def __repr__(self):
        return "<Data %s, %s, %s, %s>" % (self.date_parse, self.user_id, self.user_name, self.depth)

class InstaFollow(Base):
    __tablename__ = "instafollow"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    user_name = Column(String, nullable=False)
    follow_id = Column(Integer)
    follow_name = Column(String, nullable=False)
    #instauser = relationship("InstaUser")

    def __init__(self, user_id, user_name, follow_id, follow_name):
        self.user_id = user_id
        self.user_name = user_name
        self.follow_id = follow_id
        self.follow_name = follow_name

    def __repr__(self):
        return "<Data %s, %s, %s, %s>" % (self.user_id, self.user_name, self.follow_id, self.follow_name)

class InstaFollowed(Base):
    __tablename__ = "instafollowed"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    user_name = Column(String, nullable=False)
    followed_id = Column(Integer)
    followed_name = Column(String, nullable=False)
    #instauser = relationship("InstaUser")

    def __init__(self, user_id, user_name, followed_id, followed_name):
        self.user_id = user_id
        self.user_name = user_name
        self.followed_id = followed_id
        self.followed_name = followed_name

    def __repr__(self):
        return "<Data %s, %s, %s, %s>" % (self.user_id, self.user_name, self.followed_id, self.followed_na)


class GbParseSQLitePipeline:
    def __init__(self):
        basename = 'inst_parse'
        #engine = create_engine("sqlite:///%s" % basename, echo=False)
        engine = create_engine("sqlite:///inst_parse.db")
        #if not os.path.exists(basename):
        Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        if isinstance(item, InstaUserItem):
            dt = InstaUser(item['date_parse'], item['user_id'], item['user_name'], item['depth'])
            session = self.maker()
            session.add(dt)

        elif isinstance(item, InstaFollowItem):
            dt = InstaFollow(item['user_id'], item['user_name'], item['follow_id'], item['follow_name'])
            session = self.maker()
            session.add(dt)

        elif isinstance(item, InstaFollowedItem):
            dt = InstaFollowed(item['user_id'], item['user_name'], item['followed_id'], item['followed_name'])
            session = self.maker()
            session.add(dt)

        try:
            session.commit()
        except Exception as exc:
            print(exc)
            session.rollback()
        finally:
            session.close()
        print(1)
        #self.db[type(item).__name__].insert_one(item)
        #self.db[spider.name].insert_one(item)
        return item


#class GbParseMongoPipeline:
 #   def __init__(self):
  #      client = MongoClient()
   #     self.db = client["gb_parse_16_02_2021"]

    #def process_item(self, item, spider):
     #   self.db[type(item).__name__].insert_one(item)
        #self.db[spider.name].insert_one(item)
    #    return item

#class GbImageDownloadPipeline(ImagesPipeline):
 #   def get_media_requests(self, item, info):
  #      try:
   #         yield Request(item.get('data', ' ').get('display_url', ' '))
    #    except KeyError as ke:
     #       print(ke)
      #  except ValueError as ve:
       #     print(ve)

#    def item_completed(self, results, item, info):
 #       if results:
  #             item['data']['display_url'] = [itm[1] for itm in results]

   #     return item
