#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2023/8/31 10:29
# @Author : yzq
# @File : launch_app.py
# @Software: PyCharm
import os

from tool.glm2config.tokenization_chatglm import ChatGLMTokenizer

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:220"

import torch.cuda

from tool.file_process_tool import write_json
from tool.pre_data_process import random_message_data, pre_paper_text
from tool.prompt_engineering_collection import base_prompt, prompt_check
from transformers import AutoModel, AutoTokenizer


import streamlit as st

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6"
TITLE = "海鹰大模型AI系统"
QA_TITLE = "海鹰大模型AI问答"
logo = "./static/image/logo.png"

torch.backends.cudnn.enabled=True
torch.backends.cudnn.benchmark=True


from PIL import Image
image = Image.open('./static/image/组2.n.png')

st.set_page_config(
    page_title=TITLE,
    page_icon=logo,
    layout='wide'
)

st.image(image,caption="",width=1750)

model_name_or_path = "/home/nmnormal1/work/yzq/LLMModel/ChatGlm2_master/model/chatglm2-6b-32k"
# model_name_or_path = "/home/nmnormal1/work/yzq/LLMModel/ChatGlm2_master/model/chatglm3_6b_32k"
# model_name_or_path = "THUDM/chatglm2-6b-32k"
# model_name_or_path = "/home/nmnormal1/work/yzq/LLMModel/ChatGlm2_master/model/chatglm2-6b"


@st.cache_resource
def get_model():

    # tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
    tokenizer = ChatGLMTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
    # model = AutoModel.from_pretrained(model_name_or_path,trust_remote_code=True).cuda()

    # 多显卡支持，使用下面两行代替上面一行，将num_gpus改为你实际的显卡数量
    from utils import load_model_on_gpus
    model = load_model_on_gpus(model_name_or_path, num_gpus=7)

    model = model.eval()

    # 测试输出

    return tokenizer, model


tokenizer, model = get_model()

st.title(QA_TITLE)

# max_length = st.sidebar.slider(
#     'max_length', 0, 32768, 32768, step=1
# )
max_length=32768
# top_p = st.sidebar.slider(
#     'top_p', 0.0, 1.0, 1.0, step=0.01
# )
top_p = 0.5
# temperature = st.sidebar.slider(
#     'temperature', 0.0, 1.0, 1.0, step=0.01
# )
temperature = 0.5

if 'history' not in st.session_state:
    st.session_state.history = []

if 'past_key_values' not in st.session_state:
    st.session_state.past_key_values = None

if 'historys' not in st.session_state:
    st.session_state.historys = []

if 'QA_place' not in st.session_state:
    st.session_state.QA_place = ""

for i, (query, response) in enumerate(st.session_state.history):

    with st.chat_message(name="user", avatar="user"):
        st.markdown(query)

    with st.chat_message(name="assistant", avatar="assistant"):
        st.markdown(response)


with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()

with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()

# # 评分表单
# form = st.form(key="cofirm_point")
#
# # with col1:
# select_text = form.selectbox(label="评分", options=["0: ChatAI生成答案很糟糕，答非所问", "1: ChatAI基本能回答问题", "2: ChatAI极好地回答问题"], index=1)
#     # select_text = form.text_area(label="评分", placeholder="0:极差,1:基本,2:极好",key="select_point")
# # with col2:
# QA_placeholder = form.empty()
#
# point_button = form.form_submit_button("评分提交")
#
# if point_button:
#
#     # print(st.session_state.QA_place)
#     write_json({"QA": st.session_state.QA_place,"points": select_text}, "output/QA_point_json.json")

# 问答表单
Input_form = st.form(key="cofirm_Input")
if 'first_visit' not in st.session_state:
    st.session_state.first_visit=True
else:
    st.session_state.first_visit=False

# 初始化全局设置
if st.session_state.first_visit:
   pass

with open("data/recive.txt","r+")as f:
    txt = f.readlines()

f.close()
txt = "".join(txt)

if txt != "" :

    st.session_state.paper_txt  = txt

else:

    st.session_state.paper_txt= "目的研究乳腺一号汤剂的制备方法及质量控制,观察该制剂对乳腺增生患者的治疗效果.方法采用水提浓缩方法制备,从制剂的性状、pH值、相对浓度、鉴别、微生物限度和稳定性考察等方面进行质量控制.结果建立了乳腺一号汤剂的制备方法和质量标准.治疗100例女性乳腺增生患者,治愈42例,显效36例,好转14例,总有效率92.0%.结论该制剂制备工艺可行,治疗乳腺增生效果良好."


paper_text = Input_form.text_area(label="用户文献摘要输入",
                                  height=200,
                                  placeholder="请在这儿输入您的文献摘要信息,多个摘要请换行",
                                  value=st.session_state.paper_txt)

prompt_text = Input_form.text_area(label="用户问题输入",
                           height=100,
                           placeholder="请在这里输入您的问题，输入clear可清理历史记录")

button = Input_form.form_submit_button("发送")

if button:

    input_placeholder.markdown(prompt_text)

    if prompt_text =="" or paper_text =="":
        message_placeholder.markdown(random_message_data())

    elif prompt_text =="clear" or prompt_text=="Clear":

        st.session_state.historys = []
        st.session_state.history = []
        message_placeholder.markdown("服务器已清除缓存")

    else:

        # paper_text = "".join(paper_text.split("\n")[:2])
        check_prompt_list = base_prompt(prompt_text, paper_text)

        past_key_values,historys = st.session_state.past_key_values,st.session_state.historys

        if len(historys) > 2:

            historys = historys[-2:]

        response = ""
        responses = ""
        historys = []

        ci = 1
        for check_prompt in check_prompt_list:
            print(check_prompt)
            # check_prompt = "\n".join(check_prompt.split("\n\n")[:-2])+"@@@"
            for response, res, past_key_values in model.stream_chat(tokenizer, check_prompt, historys,
                                                                        past_key_values=past_key_values,
                                                                        max_length=max_length, top_p=top_p,
                                                                        temperature=temperature,
                                                                        return_past_key_values=True):
                message_placeholder.markdown("\n")
                message_placeholder.markdown(response)

            message_placeholder.markdown("\n")
            if len(check_prompt_list)>1:
                responses+=f"第{ci}篇:\n\n"
                ci+=1

            responses += response+"\n\n"

        torch.cuda.empty_cache() # 清理未使用的缓存

        message_placeholder.markdown(responses)

        st.session_state.QA_place = f"Q:\n{prompt_text}\nA:{responses}"

        # QA_placeholder.markdown(st.session_state.QA_place)

        write_json({"input": "\n".join(check_prompt_list), "output": responses}, "output/QA_json.json")

        st.session_state.historys = historys

        st.session_state.history.append((prompt_text,responses))

        st.session_state.past_key_values = past_key_values
