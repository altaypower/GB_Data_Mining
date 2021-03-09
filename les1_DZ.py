"""
Источник: https://5ka.ru/special_offers/
Задача организовать сбор данных,
необходимо иметь метод сохранения данных в .json файлы

результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл скачанные
данные сохраняются в Json вайлы, для каждой категории товаров должен быть создан отдельный файл и
содержать товары исключительно соответсвующие данной категории.
пример структуры данных для файла:
{
"name": "имя категории",
"code": "Код соответсвующий категории (используется в запросах)",
"products": [{PRODUCT},  {PRODUCT}........] # список словарей товаров соответсвующих данной категории
}

update
"""
import time
import json
from pathlib import Path
import requests



class Parse5Ka:
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 "
        "(Macintosh; Intel Mac OS X 10.16; rv:85.0) "
        "Gecko/20100101 Firefox/85.0",
    }

    def __init__(self, start_url: str, products_path: Path):
        self.start_url = start_url
        self.products_path = products_path

    def _get_response(self, url):
        my_count = 0
        while True:
            try:
                response = requests.get(url)
                my_count += 1
                if response.ok:
                    return response
                    time.sleep(0.5)
                elif response.status_code >= 400:
                    print('Статус - код больше 399')
                    time.sleep(0.5)
                elif my_count > 30:
                    print('Превышено количество запросов')
                    break
            # mistake for bad start_url
            except requests.exceptions.MissingSchema as rem:
                print(rem)
                break

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.products_path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    @staticmethod
    def _save(data: dict, file_path):
        jdata = json.dumps(data, ensure_ascii=False)
        file_path.write_text(jdata, encoding="UTF-8")

class CategoriesParser(Parse5Ka):
    def __init__(self, categories_url: str, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_categories(self) -> list:
        response = self._get_response(self.categories_url)
        data = response.json()
        return data

    def run(self):
        for category in self._get_categories():
            category["products"] = []
            url = f"{self.start_url}?categories={category['parent_group_code']}"
            file_path = self.products_path.joinpath(f"{category['parent_group_code']}.json")
            category["products"].extend(list(self._parse(url)))
            self._save(category, file_path)

def get_dir_path(dirname: str) -> Path:
    dir_path = Path(__file__).parent.joinpath(dirname)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    product_path = get_dir_path("products")
    cat_path = get_dir_path("categories")
    cat_url = "https://5ka.ru/api/v2/categories/"
    parser = Parse5Ka(url, product_path)
    cat_parser = CategoriesParser(cat_url, url, cat_path)
    cat_parser.run()
