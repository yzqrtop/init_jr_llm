#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2023/8/31 16:49
# @Author : yzq
# @File : pre_data_process.py
# @Software: PyCharm
import random


def random_message_data():

    list = ["请输入文献信息或问题信息", "您没有输入文献信息或问题信息，请添加相应信息。",
            "我很抱歉，您没有给定信息，无法回答！"]

    return list[random.randint(0, len(list) - 1)]

def pre_paper_text(text):

    nums = ["零","一","二","三","四","五","六","七","八","九","十"]
    # print(text)
    list = text.split("\n")
    l_len = len(list) if len(list) <20 else 20

    # print("len:",l_len)
    if l_len==1:

        list = [list[0]]

    else:

        list = [list[i]+"\n\n" for i in range(l_len)]

    return (list,"") , l_len
