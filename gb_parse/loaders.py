import re
from urllib.parse import urljoin
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

from .items import AutoyoulaItem, HHVacancyItem


def t_first(items):
    return items[0]


def get_author(item):
    re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
    result = re.findall(re_str, item)
    return urljoin("https://youla.ru/user/", result[0]) if result else None


def get_specifications(data):
    tag = Selector(text=data)
    name = tag.xpath('//div[contains(@class, "AdvertSpecs_label")]/text()').get()
    value = tag.xpath('//div[contains(@class, "AdvertSpecs_data")]//text()').get()
    return {name: value}

def specifications_out(data):
    result = {}
    for itm in data:
        result.update(itm)
    return result

class AutoyoulaLoader(ItemLoader):
    default_item_class = AutoyoulaItem
    url_out = TakeFirst()
    title_out = TakeFirst()
    description_out = TakeFirst()
    author_in = MapCompose(get_author)
    author_out = TakeFirst()
    specifications_in = MapCompose(get_specifications)
    specifications_out = specifications_out


class HHVacancyLoader(ItemLoader):
    default_item_class = HHVacancyItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_in = "".join
    description_out = TakeFirst()
    salary_in = "".join
    salary_out = TakeFirst()
