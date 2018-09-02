# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline # 下载图片

import MySQLdb # 异步Mysql存入 导包
import MySQLdb.cursors
from twisted.enterprise import adbapi # twisted框架 导包


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


# 采用同步的机制写入mysql
class MysqlPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(
            '192.168.56.101',
            'mxrain',
            'password',
            'novel',
            charset="utf8",
            use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into qidian(name, author, novel_type, crawl_time, tag, outline, novel_url, url_md5, img_url, img_url_path, novel_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["name"], item["author"], item["novel_type"], item["crawl_time"], item.get("tag",""), item["outline"], item["novel_url"], item["url_md5"], item["img_url"], item.get("img_url_path", ""), item["novel_id"]))
        self.conn.commit()


# 基于twisted异步Mysql
class MysqlTwistedPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset="utf8",
            # 不明 DictCursor这是一个游标类，它将行作为字典返回。将 结果集 存储在客户端中。
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        # 使用twisted的api
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool) # 把twisted创建的dbpool传给 self.dbpool

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


# 将数据写入到es中Pipeline
class ElasticsearchPipeline(object):

    def process_item(self, item, spider):
        # 将item转换为es的数据
        item.save_to_es()

        return item