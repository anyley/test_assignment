# -*- coding: utf-8 -*-
import scrapy


class QuokaSpider(scrapy.Spider):
    name = "quoka"
    allowed_domains = ["quoka.de"]
    start_urls = (
        'http://www.quoka.de/',
    )

    def parse(self, response):
        pass
