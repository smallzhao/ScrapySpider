import scrapy
from yangguang.items import YangguangItem


class YgrexianSpider(scrapy.Spider):
    name = 'ygrexian'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/html/top/report.shtml']

    def parse(self, response):
        contents_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table//tr")


        for c in contents_list:
            item = YangguangItem()
            item["number"] = c.xpath("./td[1]/text()").extract_first()
            item["title"] = c.xpath("./td[2]/a[2]/text()").extract_first()
            item["href"] = c.xpath("./td[2]/a[2]/@href").extract_first()
            item["author"] = c.xpath("./td[4]/text()").extract_first()
            item["publish_date"] = c.xpath("./td[3]/span/text()").extract_first()
            # 返回数据到详情页

            yield scrapy.Request(item["href"],
                                 callback=self.parse_detail,
                                 meta={"item": item})
        # 请求下一页地址
        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["content"] = response.xpath("//div[@class='c1 text14_2']//text()").extract()
        item["content_img"] = response.xpath("//div[@class='c1 text14_2']//img/@src").extract()
        item["content_img"] = ["http://wz.sun0769.com"+i for i in item["content_img"]]

        yield item