# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

class GbParsePipeline:
    def process_item(self, item, spider):
        return item


class GbParseMongoPipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client["gb_parse_16_02_2021"]

    def process_item(self, item, spider):
        self.db[type(item).__name__].insert_one(item)
        #self.db[spider.name].insert_one(item)
        return item

class GbImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        try:
            yield Request(item.get('data', ' ').get('display_url', ' '))
        except KeyError as ke:
            print(ke)
        except ValueError as ve:
            print(ve)

    def item_completed(self, results, item, info):
        if results:
               item['data']['display_url'] = [itm[1] for itm in results]

        return item
