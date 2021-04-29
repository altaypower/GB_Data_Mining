"""
Источник https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113
вакансии удаленной работы.
Задача: Обойти с точки входа все вакансии и собрать след данные:
1. название вакансии
2. оклад (строкой от до или просто сумма)
3. Описание вакансии
4. ключевые навыки - в виде списка названий
5. ссылка на автора вакансии
Перейти на страницу автора вакансии,
собрать данные:
1. Название
2. сайт ссылка (если есть)
3. сферы деятельности (списком)
4. Описание

Все вакансии авторов собрал через файл hh_company.py и добавил в коллекцию
авторов объявлений ссылку на все их вакансии
"""

import scrapy

from gb_parse.loaders import HHLoader, HHCompanyLoader
from gb_parse.spiders.xpaths import HH_PAGE_XPATH, HH_VACANCY_XPATH, HH_AUTHOR_XPATH


class HhSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://novosibirsk.hh.ru/search/vacancy?clusters=true&area=4&enable_snippets=true&salary=&st=searchVacancy&text=Data+Scientist",
        "https://novosibirsk.hh.ru/search/vacancy?area=4&clusters=true&enable_snippets=true&text=data+analyst&from=SIMILAR_QUERY",
        "https://novosibirsk.hh.ru/search/vacancy?area=4&fromSearchLine=true&st=searchVacancy&text=data+science",
        "https://novosibirsk.hh.ru/search/vacancy?clusters=true&area=4&enable_snippets=true&salary=&st=searchVacancy&text=Data+Engineer",
        "https://novosibirsk.hh.ru/search/vacancy?clusters=true&area=4&enable_snippets=true&salary=&st=searchVacancy&text=Machine+learning&from=suggest_post",
        "https://novosibirsk.hh.ru/search/vacancy?clusters=true&area=4&enable_snippets=true&salary=&st=searchVacancy&text=NLP",
        "https://novosibirsk.hh.ru/search/vacancy?clusters=true&area=4&enable_snippets=true&salary=&st=searchVacancy&text=Computer+Vision",
    ]


    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        callbacks = {"pagination": self.parse,
                     "author": self.company_parse,
                     "vacancy": self.vacancy_parse,
        }

        for key, xpath in HH_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def vacancy_parse(self, response):
        loader = HHLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in HH_VACANCY_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()

    def company_parse(self, response):
        loader = HHCompanyLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in HH_AUTHOR_XPATH.items():
            loader.add_xpath(key, xpath)

        yield loader.load_item()