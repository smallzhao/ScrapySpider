# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class ChufaSpider(CrawlSpider):
    name = 'chufa'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://www.circ.gov.cn/web/site0/tab5240/']

    rules = (
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+.htm'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/module14430/page\d+.htm'), follow=True),

    )

    def parse_item(self, response):
        item = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item["title"] = response.xpath("//table[@id='tab_content']/tbody/tr[1]/td/text()").extract()[1]
        item["publish_data"] = re.findall("发布时间：(20\d{2}-\d{2}-\d{2})", response.body.decode())
        item["publish_data"] = item["publish_data"][0] if len(item["publish_data"])>0 else None
        print(item)
        return item
