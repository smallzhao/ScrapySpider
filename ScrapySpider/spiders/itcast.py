# -*- coding: utf-8 -*-
import scrapy


class ItcastSpider(scrapy.Spider):
    """某知名培训学校师资力量"""
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    start_urls = (
        'http://www.itcast.cn/channel/teacher.shtml',
    )

    def parse(self, response):
        teachers = response.xpath("//div[@class='tea_con']//li")

        for t in teachers:
            name = t.xpath("./div/h3/text()").extract_first()
            position = t.xpath("./div/h4/text()").extract_first()
            profile = t.xpath("./div/p/text()").extract_first()

            item = dict(
                name = name,
                position = position,
                profile = profile
            )
            yield item