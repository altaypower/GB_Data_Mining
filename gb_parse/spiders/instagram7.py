"""
Источник Инстаграмм
Пройти по произвольному списку имен пользователей.
собрать в базу данных на кого подписан пользователь и кто
подписан на пользователя
"""
import datetime as dt
import json
import scrapy
from ..items import InstaUserItem, InstaFollowItem, InstaFollowedItem


class InstagramSpider(scrapy.Spider):
    name = "instagram7"
    allowed_domains = ["www.instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    api_url = "/graphql/query/"
    query_hash = {
        "follow": "d04b0a864b4b54837c0d870b0e77e076",
        "followers": "c76146de99bb02f6415203be841dd25a",
    }

    def __init__(self, login, password, *args, **kwargs):
        #self.users = ["markovsk29"]
        #self.users = ["grigorev_igor"]
        self.users = ["yakalexdmitriy"]
        #self.users = ["proskunova_anastasiya"]
        self.login = login
        self.login = login
        self.enc_passwd = password
        self.followed_list = []
        self.depth = 0
        self.depth_max = 2
        super().__init__(*args, **kwargs)

    def parse(self, response):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method="POST",
                callback=self.parse,
                formdata={
                    "username": self.login,
                    "enc_password": self.enc_passwd,
                },
                headers={"X-CSRFToken": js_data["config"]["csrf_token"]},
            )
        except AttributeError as e:
            if response.json().get("authenticated"):
                for user in self.users:
                    yield response.follow(f"/{user}/", callback=self.user_page_parse)

    def user_page_parse(self, response):
        user_data = self.js_data_extract(response)["entry_data"]["ProfilePage"][0]["graphql"]["user"]
        user_data["depth"] = self.depth
        yield InstaUserItem(date_parse=dt.datetime.utcnow(), user_id=user_data['id'], user_name=user_data['username'], depth=user_data["depth"])

        yield from self.get_api_follow_request(response, user_data)

        yield from self.get_api_followed_request(response, user_data)

    def get_api_follow_request(self, response, user_data, variables=None):
        if not variables:
            variables = {
                "id": user_data["id"],
                "first": 100,
            }
        url = f'{self.api_url}?query_hash={self.query_hash["follow"]}&variables={json.dumps(variables)}'
        yield response.follow(
            url, callback=self.get_api_follow, cb_kwargs={"user_data": user_data}
        )

    def get_api_follow(self, response, user_data):
        if b"application/json" in response.headers["Content-Type"]:
            data = response.json()
            yield from self.get_follow_item(self, user_data, data["data"]["user"]["edge_follow"]["edges"])
            if data["data"]["user"]["edge_follow"]["page_info"]["has_next_page"]:
                variables = {
                    "id": user_data["id"],
                    "first": 100,
                    "after": data["data"]["user"]["edge_follow"]["page_info"]["end_cursor"],
                }
                yield from self.get_api_follow_request(response, user_data, variables)

    @staticmethod
    def get_follow_item(self, user_data, follow_users_data):
        for user in follow_users_data:
            yield InstaFollowItem(
                user_id=user_data["id"],  # этот пользователь
                user_name=user_data["username"],
                user_depth=user_data["depth"],
                follow_id=user["node"]["id"],  # на этого пользователя
                follow_name=user["node"]["username"],
                follow_depth=(user_data["depth"] + 1),
            )
            user_name=user["node"]["username"]
            self.depth = (user_data["depth"] + 1)
            if self.depth <= self.depth_max:
                yield scrapy.Request(f"https://www.instagram.com/{user_name}/", callback=self.user_page_parse)
            else:
                self.depth -= 1
                continue

            #yield InstaUserItem(
             #   date_parse=dt.datetime.utcnow(),
              #  user_id=user["node"]["id"],
               # user_name=user["node"]["username"],
                #depth=meta['depth']
            #)

    def get_api_followed_request(self, response, user_data, variables=None):
        if not variables:
            variables = {
                "id": user_data["id"],
                "first": 100,
            }
        url = f'{self.api_url}?query_hash={self.query_hash["followers"]}&variables={json.dumps(variables)}'
        yield response.follow(
            url, callback=self.get_api_followed, cb_kwargs={"user_data": user_data}
        )

    def get_api_followed(self, response, user_data):
        if b"application/json" in response.headers["Content-Type"]:
            data = response.json()
            yield from self.get_followed_item(
                self, user_data, data["data"]["user"]["edge_followed_by"]["edges"]
            )
            if data["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"]:
                variables = {
                    "id": user_data["id"],
                    "first": 100,
                    "after": data["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"],
                }
                yield from self.get_api_followed_request(response, user_data, variables)

    @staticmethod
    def get_followed_item(self, user_data, follow_users_data, meta = {'depth': 1}):
        for user in follow_users_data:
            self.followed_list.append(user["node"]["id"])

            yield InstaFollowedItem(
                user_id=user_data["id"],  # этот пользователь
                user_name=user_data["username"],
                followed_id=user["node"]["id"],  # на этого пользователя
                followed_name=user["node"]["username"],
            )

            #yield InstaUserItem(
             #   date_parse=dt.datetime.utcnow(),
              #  user_id=user["node"]["id"],
               # user_name=user["node"]["username"],
                #meta=meta['depth']
            #)

    @staticmethod
    def js_data_extract(response):
        script = response.xpath('//script[contains(text(), "window._sharedData =")]/text()').get()
        return json.loads(script.replace("window._sharedData =", "")[:-1])
