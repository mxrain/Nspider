#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/1 0001 14:27
# @Author  : Mxrain

def return_value(value):
    return value

def return_img_ls(value):
    ls= []
    ls.append("https:"+value.strip())
    return ls

if __name__=="__main__":
    print(return_value(['1','2','3']))