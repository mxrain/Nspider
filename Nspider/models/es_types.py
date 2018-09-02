#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/1 0001 16:21
# @Author  : Mxrain
from elasticsearch_dsl import DocType, Completion, Text, Date, Keyword, Integer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"]) # 连接hosts

class QidianType(DocType):
    #起点中文网类型

    # suggest = Completion(analyzer=ik_analyzer)
    name = Text(analyzer="ik_max_word")
    author = Text(analyzer="ik_max_word")
    novel_type = Text(analyzer="ik_max_word")
    crawl_time = Date()
    tag = Text(analyzer="ik_max_word")
    outline = Text(analyzer="ik_max_word")
    novel_url = Keyword()
    url_md5 = Keyword()
    img_url = Keyword()
    img_url_path = Keyword()
    novel_id = Keyword()

    class Meta: # 连接index（db） 和 type（table）
        index = "novel"
        doc_type = "qidian"

    class Index:
        name = 'novel'
        doc_type = "qidian"

if __name__ == "__main__":
    QidianType.init() # 创建mappings
