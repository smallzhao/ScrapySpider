# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        with open('temp.txt', 'a') as f:
            print(item)
            json.dump(item, f, ensure_ascii=False, indent=2)
        # return item
