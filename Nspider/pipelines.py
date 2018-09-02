# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline


class NspiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 图片下载pipeline
class NimgPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        if "img_url" in item:
            for ok,value in results:
                imge_file_path = value["path"]
            item["img_url_path"] = imge_file_path
        return item


# 将数据写入到es中Pipeline
class ElasticsearchPipeline(object):

    def process_item(self, item, spider):
        # 将item转换为es的数据
        item.save_to_es()

        return item