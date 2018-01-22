# -*- coding: utf-8 -*-
import scrapy, re
from copy import deepcopy


class SnspiderSpider(scrapy.Spider):
    name = 'snspider'
    allowed_domains = ['www.suning.com', 'snbook.suning.com']
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):
        title_list = response.xpath("//li[contains(@class, 'lifirst')]")

        for t in title_list:
            item = {}
            item["b_title"] = t.xpath("./div[1]/a/text()").extract_first()

            l_title_list = t.xpath("./div[2]/a")
            for b in l_title_list:
                item["l_href"] = b.xpath("./@href").extract_first()
                item["l_title"] = b.xpath("./text()").extract_first()
                if item["l_href"] is not None:
                    item["l_href"] = "http://snbook.suning.com" + item["l_href"]
                    yield scrapy.Request(
                        item["l_href"],
                        callback=self.parse_detail,
                        meta={"item": deepcopy(item)}
                    )

    def parse_detail(self, response):
        item = response.meta["item"]
        books_list = response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for b in books_list:
            item["book_name"] = b.xpath(".//div[@class='book-title']/a/@title").extract_first()
            item["book_img"] = b.xpath(".//div[@class='book-img']/img/@src").extract_first()
            item["book_author"] = b.xpath(".//div[@class='book-author']/a/text()").extract_first()
            item["book_publish"] = b.xpath(".//div[@class='book-publish']/a/text()").extract_first()
            item["book_descrip"] = b.xpath(".//div[@class='book-descrip c6']/text()").extract_first()
            item["book_href"] = b.xpath(".//div[@class='book-title']/a/@href").extract_first()

            if item["book_href"] is not None:

                yield scrapy.Request(
                    item["book_href"],
                    callback=self.parse_price,
                    meta={"item": deepcopy(item)}
                )
        # 下一页
        page_count = int(re.findall("var pagecount=(.*?);", response.body.decode())[0])
        current_page = int(re.findall("var currentPage=(.*?);", response.body.decode())[0])
        if current_page < page_count:
            next_url = item["l_href"] + "?pageNumber={}&sort=0".format(current_page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse_detail,
                meta={"item": item}
            )

    def parse_price(self, response):

        item = response.meta["item"]
        print(item)
        item["book_price"] = re.findall(r"\"bp\":'(.*?)',", response.body.decode())
        item["book_price"] = item["book_price"][0] if len(item["book_price"])>0 else None

        yield item