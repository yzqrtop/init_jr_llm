# -*- coding: utf-8 -*-
# @Time    : 2024/5/25 15:06
# @Author  : yzqrtop
# @FileName: main_glm_server.py
# @Software: PyCharm
# @Blog    ：https://blog.csdn.net/weixin_44077556?type=blog
from fastapi import FastAPI, Body
import uvicorn

from tool.glm2config.modeling_chatglm import logger
from tool.glm2config.tokenization_chatglm import ChatGLMTokenizer
import os
import json
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7"
# port = 8885
port = 8888
debug = False

app = FastAPI()
model_name_or_path = "/home/nmnormal1/work/yzq/LLMModel/ChatGlm2_master/model/chatglm2-6b-32k"
# tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
tokenizer = ChatGLMTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
# model = AutoModel.from_pretrained(model_name_or_path,trust_remote_code=True).cuda()

# 多显卡支持，使用下面两行代替上面一行，将num_gpus改为你实际的显卡数量
from utils import load_model_on_gpus
model = load_model_on_gpus(model_name_or_path, num_gpus=8)

model = model.eval()
# tokenizer,model = None,None
# ml_models = {}
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Load the ML model
#     from tool.llm_tool.llm_streamQA_tokenizer import tokenizer, model
#     ml_models["tokenizer"] = tokenizer
#     ml_models["model"] = model
#     yield
#     # Clean up the ML models and release the resources
#     ml_models.clear()
# app = FastAPI(lifespan=lifespan)

#
# @app.post("/recive_stream/{parameter}")
# async def recive_stream(parameter, abstracts=Body(), question=Body(), id=Body(default=""), type=Body(default=""),
#                         userId=Body(default=""),
#                         userLibCode=Body(default=""), userType=Body(default=""), accessLibCode=Body(default=""),
#                         userAgent=Body(default=""), ip=Body(default="")):
#     # @stream_with_context
#     # 流式获取单个答案
#     def get_stream_answer(tokenizer, model, question_text, paper_text):
#         """
#         :param tokenizer: 模型向量
#         :param model: 模型
#         :param question_text: 问题
#         :param paper_text: 文章列表
#         :return:
#         """
#         # logger.info('GLM parameter: %s' % parameter)
#         # logger.info('GLM question: %s' % question_text)
#         # logger.debug('GLM abstracts: %s' % paper_text)
#         # print("========================================direct:",id, '=====', type)
#         interface = "recive_stream-" + parameter
#         responses = ""
#         size = 0
#         if parameter == "mul_QA":
#             ci = 0
#
#             for paper in paper_text:
#                 query = f"<{paper}>\n{question_text}"
#                 yield "<p>"
#                 responses += "<p>"
#                 for response, historys, past_key_values in model.stream_chat(tokenizer, query, [],
#                                                                              return_past_key_values=True):
#                     response = response.replace("\n", "<br/>")
#                     this_response = response[size:]
#                     size = len(response)
#                     yield this_response
#
#                 responses += response
#                 yield f"<a herf='#{str(ci + 1)}'/><br/><p/>"
#                 responses += f"<a herf='#{str(ci + 1)}'/><br/><p/>"
#                 ci += 1
#
#         else:
#
#             query = f'<{"".join(paper_text)}>\n{question_text}'
#
#             for response, historys, past_key_values in model.stream_chat(tokenizer, query, [],
#                                                                          return_past_key_values=True):
#                 response = response.replace("\n", "<br/>")
#                 this_response = response[size:]
#                 size = len(response)
#                 yield this_response
#
#             responses += response
#
#             # print("res", responses)
#         log_request(interface, {'text': responses}, question=question_text, abstracts=paper_text, id=id, type=type,
#                     userId=userId, userLibCode=userLibCode, userType=userType, accessLibCode=accessLibCode,
#                     userAgent=userAgent, ip=ip)
#
#     def Error_return(question_text, paper_text, error):
#         log_request('recive_stream-' + parameter, {'text': error}, question=question_text, abstracts=paper_text,
#                     id=id, type=type,
#                     userId=userId, userLibCode=userLibCode, userType=userType, accessLibCode=accessLibCode,
#                     userAgent=userAgent, ip=ip)
#         yield error
#
#     form = {"abstracts": abstracts, "question": question}
#
#     try:
#         # if len(abstracts)>1:
#         #    if type(abstracts[0]) != str:
#         #        return EventSourceResponse(Error_return(question, abstracts, "请输入正确摘要格式", ))
#         if isinstance(abstracts, list):
#             Error_return(question, abstracts, "请输入正确摘要格式")
#
#         abstracts = form["abstracts"]  # 列表
#         question = form["question"]  # 字符
#
#         return EventSourceResponse(get_stream_answer(tokenizer, model, question, abstracts))
#     except Exception as e:
#         traceback.print_exc()
#         return EventSourceResponse(Error_return(question, abstracts, e))


# async

@app.post("/recive_stream/sig_QA/direct")
async def recive_direct_answer(prompt=Body()):

    question = prompt["prompt"]
    responses = []

    res = {"code": -1, "msg": "", "count": len(responses), "data": responses}

    try:
        query = f'{question}'
        response = ""

        for response, historys, past_key_values in model.stream_chat(tokenizer, query, [], return_past_key_values=True):
            pass

        response = response.replace("\n", "<br/>")
        responses.append(response)
        logger.info(f"question:{question}")
        res = {"code": 0, "msg": "success", "count": len(responses), "data": responses}

    except Exception as e:
        # res['msg'] = str(e)
        response = str(e)

    # return json.dumps({"text":response})
    return response


if __name__ == '__main__':
    uvicorn.run(app="main_glm_server:app", host="0.0.0.0", port=port, workers=1, limit_concurrency=200)
