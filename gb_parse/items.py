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
    data = scrapy.Field()
    photos = scrapy.Field()


class InstaTag(Insta):
    pass

class InstaPost(Insta):
    pass

class InstaUser(Insta):
    pass

class InstaFollow(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    follow_name = scrapy.Field()
    follow_id = scrapy.Field()

class InstaFollowed(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    followed_name = scrapy.Field()
    followed_id = scrapy.Field()
