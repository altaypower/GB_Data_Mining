from scrapy.loader import ItemLoader
from urllib.parse import urljoin
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose, Join
#from .items import GbAutoYoulaItem
from .items import GbHHItem, GbHHCompanyItem, GbHHCmpItem


def get_characteristics(item):
    selector = Selector(text=item)
    data = {
        "name": selector.xpath(
            "//div[contains(@class, 'AdvertSpecs_label')]/text()"
        ).extract_first(),
        "value": selector.xpath(
            "//div[contains(@class, 'AdvertSpecs_data')]//text()"
        ).extract_first(),
    }
    return data


def create_user_url(user_id):
    return urljoin("https://youla.ru/user/", user_id)


def clear_price(price: str) -> float:
    try:
        return float(price.replace("\u2009", ""))
    except ValueError:
        return float("NaN")


class AutoyoulaLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    characteristics_in = MapCompose(get_characteristics)
    author_in = MapCompose(create_user_url)
    author_out = TakeFirst()
    price_in = MapCompose(clear_price)
    price_out = TakeFirst()
    descriptions_out = TakeFirst()


def flat_text(items):
    return "\n".join(items)


def hh_user_url(user_id):
    return urljoin("https://hh.ru/", user_id)


class HHLoader(ItemLoader):
    default_item_class = GbHHItem
    #default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = flat_text
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()

def split_text(items):
    return items[0].split(',')

def flat_title(items):
    return items[0] + items[1]


class HHCompanyLoader(ItemLoader):
    default_item_class = GbHHCompanyItem
    url_out = TakeFirst()
    title_out = flat_title
    site_out = TakeFirst()
    activity_out = split_text
    description_out = Join()
    vacancies_in = MapCompose(hh_user_url)
    vacancies_out = TakeFirst()


class HHCmpLoader(ItemLoader):
    default_item_class = GbHHCmpItem
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = flat_text
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()