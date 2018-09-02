# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from Nspider.Utils.item_common import return_value, return_img_ls, return_strip
from Nspider.models.es_types import QidianType


class NspiderItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    pass

class NspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    author = scrapy.Field()
    novel_type = scrapy.Field(
        output_processor=Join(",")
    )
    crawl_time = scrapy.Field()
    tag = scrapy.Field(
        output_processor=MapCompose(Join,return_strip),
    )
    outline = scrapy.Field(
        output_processor=Join(","),
        input_processor=MapCompose(return_strip)
    )
    novel_url = scrapy.Field()
    url_md5 = scrapy.Field()
    img_url = scrapy.Field(
        input_processor=MapCompose(return_img_ls),
        output_processor=MapCompose(return_value)
    )
    img_url_path = scrapy.Field()
    novel_id = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    insert into qidian(name, author, novel_type, crawl_time, tag, outline, novel_url, url_md5, img_url, img_url_path, novel_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        params = (self['name'], self["author"], self["novel_type"], self["crawl_time"], self.get("tag",""), self["outline"], self["novel_url"], self["url_md5"], self["img_url"], self.get("img_url_path",""), self["novel_id"])

        return insert_sql, params



    def save_to_es(self):
        novel = QidianType()
        novel.name = self['name']
        novel.author = self["author"]
        novel.novel_type = self["novel_type"]
        novel.crawl_time = self["crawl_time"]
        if "tag" in self:
            novel.tag = self.get("tag","")
        novel.outline = self["outline"]
        novel.novel_url = self["novel_url"]
        novel.url_md5 = self["url_md5"]
        novel.img_url = self["img_url"]
        novel.img_url_path = self.get("img_url_path","")
        novel.novel_id = self["novel_id"]
        # article.suggest = gen_suggests(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
        novel.save()
        # redis_cli.incr("jobbole_count")

        return