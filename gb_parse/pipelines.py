# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo


class MongoPipeline:
    def __init__(self):
        self.db = pymongo.MongoClient()['gb_parse_16_12_2020']

    def process_item(self, item, spider):
        if not self.db[item.__class__.__name__].count({'url': item['url']}):
            self.db[item.__class__.__name__].insert_one(item)
        return item
