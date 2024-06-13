#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2023/9/1 14:39
# @Author : yzq
# @File : file_process_tool.py
# @Software: PyCharm
import json

def write_json(data, path):

    try:

        with open(path, "a+",encoding="utf-8") as f:
            json.dump(data, f)
            f.writelines("\n")
        f.close()


    except Exception as e:
        print(e)