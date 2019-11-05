# -*- coding: utf-8 -*-
import scrapy


class GardenSpider(scrapy.Spider):
    name = 'garden'
    allowed_domains = ['gar-den.in/']
    start_urls = ['http://gar-den.in/']

    def parse(self, response):
        pass
