#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/1 0001 12:56
# @Author  : Mxrain

import hashlib
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def get_id(url):
    # 从url中提取id
    if isinstance(url,str):
        url = url.rsplit("/",1)
    return url.pop()



if __name__=="__main__":
    print(get_md5("https://book.qidian.com/info/1012390525"))
    print(get_id("https://book.qidian.com/info/1012390525"))