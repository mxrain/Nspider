# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Nspider.Utils.common import get_md5, get_id
from Nspider.items import NspiderItemLoader, NspiderItem


class QidianSpider(CrawlSpider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com',
                       'www.qdmm.com',
                       'book.qidian.com'
                       ]
    start_urls = ['http://www.qidian.com/']
    rules = (
        Rule(LinkExtractor(allow=r'info/\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        item_loader = NspiderItemLoader(item=NspiderItem(),response=response)
        item_loader.add_css("name","div.book-info h1 em::text")
        item_loader.add_css("author","div.book-info h1 a::text")
        item_loader.add_css("novel_type","div.book-info p.tag a::text")
        item_loader.add_value("crawl_time",datetime.now())
        item_loader.add_css("tag","a.tags::text")
        item_loader.add_css("outline","div.book-intro p::text")
        item_loader.add_value("novel_url",response.url)
        item_loader.add_value("url_md5",get_md5(response.url))
        item_loader.add_css("img_url","div.book-information div.book-img img::attr(src)")
        item_loader.add_value("novel_id", get_id(response.url))
        item_loader.add_value("img_url_path", "")

        novel_item = item_loader.load_item()

        yield novel_item
