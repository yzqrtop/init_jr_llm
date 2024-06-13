#!C:\pythonCode
# -*coding: utf-8 -*-
# @Time : 2023/8/31 11:17
# @Author : yzq
# @File : prompt_engineering_collection.py
# @Software: PyCharm
from tool.pre_data_process import pre_paper_text

def base_prompt(prompt,inputs):

    (paper_list,p_num), llen = pre_paper_text(inputs)

    check_prompt = prompt_check(prompt, llen)

    # print(check_prompt)
    # system_prompt = "你是一个助手，你的回答必须根据用户的问题输出，不要添加任何说明信息。\n 如果无法解答问题，请回答后面一句话。‘’‘您的问题不在JRChatAI赋予的问答权限范围内’‘’。\n"
    system_prompt = "你是一个助手，你的回答必须根据用户的问题输出，不要添加任何说明信息。\n"

    if len(check_prompt)==1: # 当提示为单个时，合并所有文献为一个。
        paper_list = ["".join(paper_list)]

    base_prompt_list = []

    for check_i in range(len(check_prompt)):

        # print(check_i,len(check_prompt),len(paper_list))

        texts = f'{system_prompt}\n'
        strs = f"{check_prompt[check_i]}\n@@@{paper_list[check_i]}@@@"
        texts += strs
        base_prompt_list.append(texts)

        # print(texts)
    return base_prompt_list

def prompt_check(prompt,llen):

    if llen==1:

        return single_QA_check(prompt)

    elif llen>1:

        return multiple_QA_check(prompt,llen)

    else:

        return prompt

def single_QA_check(prompt):

    # verbs = ["总结","生成"]
    # for i in verbs:
    #     if verbs in prompt:

    batch_prompts_keys = ["题目", "标题", "名字", "实体", "关键词", "关系","方法","目的","结果","结论"]

    all_prompts_keys = [{"key": ["结构"], "value": ["目的","方法","结果","结论"],"batch_prompt":f"根据@@@里内容，请用中文按照下面格式生成：\n "},
                        {"key":["概述"],"value": ["题目", "关键词", "结果","结论","目的","方法"],"batch_prompt":f"根据@@@里内容，请用中文按照下面格式生成：\n "},
                        {"key":["专利"],"value": ["题目","技术领域", "背景","专利概述","专利内容","专利步骤","专利实施方式","专利要求","专利描述",
                                                         "题目撰写建议","技术领域撰写建议", "背景撰写建议","专利概述撰写建议",
                                                         "专利内容撰写建议","专利步骤撰写建议","专利实施方式撰写建议",
                                                         "专利要求撰写建议","专利描述撰写建议"],"batch_prompt":f"根据@@@里内容，请用中文按照下面格式生成：\n "},
                        {"key": ["中文综述"],
                         "value": ["引言-概述领域", "引言-背景", "引言-提出问题", "引言-综述目的", "文献综述-回顾文献",
                                   "文献综述-研究方法总结", "方法理论及原理", "实证研究-研究设计", "数据收集",
                                   "分析方法", "讨论", "改进方向", "主要意义", "未来方向","参考文献"],"batch_prompt":f"根据@@@里内容，请用中文按照下面格式生成：\n "},
                        {"key": ["英文综述"],
                         "value": ["introduce", "target", "question describe", "background", "research methods", "result", "discussion and analysis",
                                   "conclusion","reference"],
                         # "value": ["引言-概述领域", "引言-背景", "引言-提出问题", "引言-综述目的", "文献综述-回顾文献",
                         #           "文献综述-研究方法总结", "方法理论及原理", "实证研究-研究设计", "数据收集",
                         #           "分析方法", "讨论", "改进方向", "主要意义", "未来方向", "参考文献"],
                         "batch_prompt":f"根据@@@里内容，请用英文按照下面格式生成：\n\n"}
                        ]

    for i in batch_prompts_keys:
        if i in prompt:
            # print(batch_prompt)
            return [f"根据@@@里内容，按照下面格式生成:\n# 【{i}】\n- ‘’‘{i}’‘’\n\n"]


    for i in all_prompts_keys:
        for j in i["key"]:
            if j in prompt:
                batch_prompt = i["batch_prompt"]

                for k in i["value"]:

                    batch_prompt += f"【{k}】:'''{k}'''\n\n"

                return [batch_prompt]

    return [prompt]


def multiple_QA_check(prompt, llen):
    # lists = ["目的",]
    # res = f"根据多个三引号里内容，按照下面格式生成：\n【目的区别】：根据多个三引号里内容，生成目的区别\n【关键词区别】：根据多个三引号里内容，生成关键词区别\n【方法区别】：根据多个三引号里内容，生成方法区别\n【结果区别】：根据多个三引号里内容，生成结果区别\n【内容相似性】：根据多个三引号里内容，回答哪几篇文献比较相似\n"
    # batch_prompt = f"根据多个@@@内容，如果无法解答问题，请生成：\n'''请详细描述，例如关键词区别，方法相似处等'''，\n如果理解则按照下面格式生成：\n尊敬的JRChatAI用户，根据您的问题【{prompt}】回答如下：‘’‘{prompt}’‘’\n"

    all_prompts_keys = [{"key": ["专利"], "value": ["题目", "技术领域", "背景", "专利概述", "专利内容", "专利步骤", "专利实施方式",
                                   "专利要求", "专利描述",
                                   "题目撰写建议", "技术领域撰写建议", "背景撰写建议", "专利概述撰写建议",
                                   "专利内容撰写建议", "专利步骤撰写建议", "专利实施方式撰写建议",
                                   "专利要求撰写建议", "专利描述撰写建议"],"batch_prompt":f"根据@@@里内容，请用中文按照下面格式生成：\n "},
                        {"key": ["中文综述"],
                         "value": [ "引言-背景", "引言-综述目的", "文献综述-回顾文献",
                                   "文献综述-方法理论及原理", "实证研究-研究设计", "讨论","主要意义", "未来方向","参考文献"],"batch_prompt":f"根据@@@里内容，请用中文按照下面格式生成：\n "},
                        {"key": ["英文综述"],
                         "value": ["introduce", "target", "background", "research methods",
                                   "result", "conclusion","reference"]
                         # "value": ["引言-概述领域", "引言-背景", "引言-提出问题", "引言-综述目的", "文献综述-回顾文献",
                         #           "文献综述-研究方法总结", "方法理论及原理", "实证研究-研究设计", "数据收集",
                         #           "分析方法", "讨论", "改进方向", "主要意义", "未来方向", "参考文献"]
                            ,"batch_prompt":f"根据@@@里内容，请用英文按照下面格式生成：\n\n"}
                        ]

    # ra
    # 撰写多篇文献一起总结的模版
    for i in all_prompts_keys:

        for j in i["key"]:

            if j in prompt:

                batch_prompt = i["batch_prompt"]

                for k in i["value"]:

                    batch_prompt += f"【{k}】:'''{k}'''\n\n"

                return [batch_prompt]


    # 撰写多篇文献分别总结的提示模版
    batch_prompts_keys = ["题目", "标题", "名字", "实体", "关键词", "关系", "方法", "目的", "结果", "结论"]

    struct_prompt = [{"key": ["结构"], "value": ["目的", "方法", "结果", "结论"]},
                     {"key": ["概述"], "value": ["题目",  "结论", "目的", "方法"]}]
    batch_prompt_list = []

    is_single = False
    # 撰写多篇文献分别问答的单类别结构提示
    for i in range(llen):
        for key in batch_prompts_keys:
            if key in prompt:
                batch_prompt = "根据@@@内容，按照下面格式回答: \n"
                batch_prompt+=f"# 【{key}】: '''{key}'''\n\n"
                batch_prompt_list.append(batch_prompt)
                is_single = True
                break


    if is_single:
        return batch_prompt_list

    is_multiple = False
    batch_prompt_list = []
    for i in range(llen):
        # 撰写多篇文献分别问答的多类别结构提示
        for data in struct_prompt:
            for key in data["key"]:

                if key in prompt:

                    batch_prompt = f"根据@@@内容，按照下面格式回答: \n"

                    for val in data["value"]:

                        batch_prompt += f"【{val}】: '''{val}'''\n\n"

                    batch_prompt_list.append(batch_prompt)
                    is_multiple = True
    if is_multiple:
        return batch_prompt_list

    return [f"根据@@@里内容,按照下面格式生成：\n# 【{prompt}】\n\n- 生成{prompt}\n"]