#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2023/8/31 11:14
# @Author : yzq
# @File : test.py
# @Software: PyCharm
import json

# import wandb
# wandb_project = "JR_Chat_Log"
# wandb_name = "one_high_QA_Collection"
#
# wandb.init(project=wandb_project,name=wandb_name)
#
# wandb.log({"Question":"测试","Answer":"测试3"})
# wandb.log({"Question":"测试","Answer":"测试1"})
# wandb.log({"Question":"测试","Answer":"测试2"})
#
# table = wandb.Table(columns=["Quq","Ans","point"])
# table.add_data("c1","a","sf")
# wandb.log({"output_validation_table":table})
#
# table.add_data("c2","a","sfa")
# table.add_data("c3","as","sfa")
# wandb.log({"output_validation_table":table})
#
# table.add_data("c4","a","sfa")
# table.add_data("c5","as","sfa")
# wandb.log({"output_validation_table":table})
# wandb.log({"Question":"测试","Answer":"测试2","point":"3"})
# wandb.finish()
data = [{"input":"jieguo","output":"jieguo"},{"input":"jieguo","output":"jieguo"},{"input":"jieguo","output":"jieguo"}]

with open("a.json","a+")as f:
    
    json.dump(data,f)
    f.writelines("\n")

f.close()

data = [{"input":"jieguo","output":"jieguo"},{"input":"jieguo","output":"jieguo"},{"input":"jieguo","output":"jieguo"}]

with open("a.json","a+")as f:
    json.dump(data, f)
    f.writelines("\n")
f.close()

