# -*- coding: utf-8 -*-
import scrapy
import logging

# from scrapy.loader import ItemLoader
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor as sle
# from scrapy.selector import HtmlXPathSelector
# from scrapy.loader.processors import TakeFirst

from test_assignment.items import QuokaItem


# class QuokaLoader(ItemLoader):
#     default_output_processor = TakeFirst()


class QuokaSpider(scrapy.spiders.CrawlSpider):
    name = "quoka"
    allowed_domains = ["quoka.de"]
    start_urls = (
        'http://www.quoka.de/immobilien/bueros-gewerbeflaechen',
    )

    # def parse(self, response):
    #     return [scrapy.FormRequest(url=response.url,
    #                                formdata={'classtype': 'of'},
    #                                callback=self.changeCity)]

    def parse(self, response):
        logging.info('change city')
        logging.info(response.css('.modal-header.col-xs-search')
                             .xpath('div/text()')
                             .extract())

        for city in response.xpath('//a[contains(@onclick,"qsn.changeCity")]/@href'):
            url = response.urljoin(city.extract())
            logging.info(url)
            for comm in ('0'):
                yield scrapy.FormRequest(
                    url,
                    formdata={
                        'classtype': 'of',
                        'comm': comm
                    },
                    callback=self.after_filter)
            return

    def after_filter(self, response):
        logging.info('after_filter: %s', response.url)
        logging.info(response.css('.modal-header.col-xs-search')
                             .xpath('div/text()')
                             .extract())

        # path = response.xpath('//li[@class="arr-rgt active"]/a/@href').extract()
        # if len(path) > 0:
        #     url = response.urljoin(path[0])
        #     logging.info(url)
        #     scrapy.Request(url, callback=self.next_page)
        self.next_page(response)
        return

        for href in response.css('a.qaheadline.item.fn::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)

    def next_page(self, response):
        logging.info('next_page: %s', response.url)
        logging.info(response.css('.modal-header.col-xs-search')
                             .xpath('div/text()')
                             .extract())
        path = response.xpath('//li[@class="arr-rgt active"]/a/@href').extract()
        logging.info("Path: %i", len(path))
        if len(path) > 0:
            url = response.urljoin(path[0])
            logging.info("URL: %s", url)
            scrapy.Request(url, callback=self.next_page)

    def parse_item(self, response):
        # logging.info("Parse ITEM: " + response.url)
        item = QuokaItem()
        item['href'] = response.url
        # l = ItemLoader(item=QuokaItem(), response=response)
        yield item
