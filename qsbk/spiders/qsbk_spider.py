# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList
from qsbk.items import QsbkItem

class QsbkSpiderSpider(scrapy.Spider):
    name = 'qsbk_spider'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1']
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        datas = response.xpath("//div[@class='col1 old-style-col1']/div")
        for data in datas:
            author = data.xpath(".//div[@class='author clearfix']//h2/text()").get().strip()
            content = data.xpath(".//a[@class='contentHerf']/div[@class='content']//text()").getall()
            content = "".join(content).strip()
            item = QsbkItem(author=author,content=content)
            yield item
            next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
            print("=======next_url======")
            print(next_url)
            if not next_url:
                return
            else:
                yield scrapy.Request(self.base_domain + next_url,callback=self.parse)
