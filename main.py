#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/1 0001 13:34
# @Author  : Mxrain


import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","qidian"])