# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Join


class GbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GbAutoYoulaItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field()
    photos = scrapy.Field()
    characteristics = scrapy.Field()
    descriptions = scrapy.Field()
    author = scrapy.Field()


class GbHHItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    author = scrapy.Field(output_processor=TakeFirst())

class GbHHCompanyItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field()
    site = scrapy.Field(output_processor=TakeFirst())
    activity = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=Join())
    vacancies = scrapy.Field(output_processor=TakeFirst())


class GbHHCmpItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field()
    description = scrapy.Field()
    skills = scrapy.Field()
    author = scrapy.Field(output_processor=TakeFirst())

class Insta(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    #data = scrapy.Field()
    #photos = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()

class InstaUserItem(Insta):
    date_parse = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    depth = scrapy.Field()

class InstaFollowItem(scrapy.Item):
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_depth = scrapy.Field()
    follow_id = scrapy.Field()
    follow_name = scrapy.Field()
    follow_depth = scrapy.Field()

class InstaFollowedItem(scrapy.Item):
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    followed_name = scrapy.Field()
    followed_id = scrapy.Field()

class InstaUserItem2(Insta):
    date_parse = scrapy.Field()
    user_id2 = scrapy.Field()
    user_name2 = scrapy.Field()
    depth2 = scrapy.Field()

class InstaFollowItem2(scrapy.Item):
    user_id2 = scrapy.Field()
    user_name2 = scrapy.Field()
    user_depth2 = scrapy.Field()
    follow_id2 = scrapy.Field()
    follow_name2 = scrapy.Field()
    follow_depth2 = scrapy.Field()

class InstaFollowedItem2(scrapy.Item):
    user_name2 = scrapy.Field()
    user_id2 = scrapy.Field()
    followed_name2 = scrapy.Field()
    followed_id2 = scrapy.Field()

class InstaTag(Insta):
    pass

class InstaPost(Insta):
    pass