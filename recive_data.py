#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2023/9/13 15:59
# @Author : yzq
# @File : recive_data.py
# @Software: PyCharm

import datetime
import time

import requests
from flask import Flask, request
from gevent.pywsgi import WSGIServer

app=Flask(__name__)

@app.route('/',methods=["post","get"])
def index():
    return 'welcome to my webpage!'

@app.route("/recive",methods=["post","get"])
def recive():
    form = request.json
    # form = request.form
    # print(form)
    # abstract = request.args.get("abstracts")
    abstracts = form["abstracts"]
    # time = datetime.datetime.now()
    # print(abstracts)
    try:
        with open(f"data/recive.txt","w") as f:
            f.writelines(str(abstracts))
        f.close()
    except Exception as e:
        print(e)
        return "error"
    return "success"

if __name__=="__main__":

    # app.run(port=8880,host="0.0.0.0",threaded=False,debug=True)
    #
    server = WSGIServer(('0.0.0.0', 8880), app)
    print('=============server started=============')
    print('=============127.0.0.0:8880=============')
    server.serve_forever()