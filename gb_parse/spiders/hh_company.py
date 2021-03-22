
import scrapy

from gb_parse.loaders import HHCmpLoader
from gb_parse.spiders.xpaths import HH_PAGE_COMP_XPATH, HH_COMPANY_XPATH, HH_VACANCY_XPATH, HH_VAC_PAGE_XPATH


class HhCmpSpider(scrapy.Spider):
    name = "hh_company"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://novosibirsk.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113"
    ]
    #start_urls = [
     #   "https://novosibirsk.hh.ru/employer/3361389"
    #]


    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        callbacks = {"pagination": self.parse,
                     "author": self.companies_parse,
        }

        for key, xpath in HH_PAGE_COMP_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def companies_parse(self, response):
        yield from self._get_follow_xpath(
            response, HH_COMPANY_XPATH["vacancies"], self.cmp_parse
        )

    def cmp_parse(self, response):
        callbacks = {"pagination": self.parse,
                     "vacancy": self.vacancion_parse,
        }

        for key, xpath in HH_VAC_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])


    def vacancion_parse(self, response):
        loader = HHCmpLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in HH_VACANCY_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()
