# -*- coding: utf-8 -*-
import scrapy
from amazon_scrapy.items import AmazonItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/s/field-keywords=mobile%20phone']


    def parse(self, response):
        title = response.xpath("//div[@class='a-row a-spacing-none scx-truncate-medium sx-line-clamp-2']//a[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']//h2/text()").extract()
        price = response.xpath(
            "//div[@class='a-row a-spacing-none']//a[@class='a-link-normal a-text-normal']//span[@class='a-offscreen']/text()").extract()
        link = response.xpath("//div[@class='a-row a-spacing-none scx-truncate-medium sx-line-clamp-2']//a[@class='a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal']/@href").extract()
        image = response.xpath("//div[@class='a-column a-span12 a-text-center']//a[@class='a-link-normal a-text-normal']//img[@class='s-access-image cfMarker']/@src").extract()

        for item in zip(title,price,link,image):
            new_item = AmazonItem()
            new_item['title'] = item[0]
            new_item['price'] = item[1]
            new_item['link'] = item[2]
            new_item['image'] = item[3]
            yield new_item

        next_page = response.xpath(
            "//div[@class='pagnHy']//span[@class='pagnRA']//a[@class='pagnNext']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)