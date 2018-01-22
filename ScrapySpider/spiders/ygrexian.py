# -*- coding: utf-8 -*-
import scrapy


class YgrexianSpider(scrapy.Spider):
    name = 'ygrexian'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/html/top/report.shtml']

    def parse(self, response):
        contents_list = response.xpath("//div[@class='greyframe']/table[2]/tbody/tr/td//tr")

        for c in contents_list:

            pass
