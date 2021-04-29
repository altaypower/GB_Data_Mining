# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class GbParsePipeline:
    def process_item(self, item, spider):
        return item

#class DuplicatesPipeline:
#
 #   def __init__(self):
  #      self.ids_seen = set()
#
 #   def process_item(self, item, spider):
  #      adapter = ItemAdapter(item)
   #     if adapter['url'] in self.ids_seen:
    #        raise DropItem(f"Duplicate item found: {item!r}")
     #   else:
      #      self.ids_seen.add(adapter['url'])
       #     return item


class GbParseMongoPipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client["gb_parse_16_02_2021"]

    def process_item(self, item, spider):
        self.db[type(item).__name__].insert_one(item)
        #self.db[spider.name].insert_one(item)
        return item

