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


# 从url中提取id
def get_id(url):
    if isinstance(url,str):
        url = url.rsplit("/",1)
    return int(url.pop())


# 从字符串中提取出数字
def extract_num(text):
    match_re = re.match(".*?(\d+).*", text)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


if __name__=="__main__":
    print(get_md5("https://book.qidian.com/info/1012390525"))
    print(get_id("https://book.qidian.com/info/1012390525"))