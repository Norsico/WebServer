import json

import requests

API_KEY = "o8Wk9BRgMvF9b2NdLYryU6gc"
SECRET_KEY = "yZw1jvh9DhkRefj1Mx28CnQD8XC7pDqO"


# massage = \
#     {
#         "messages": [
#             {"role": "user", "content": "你好"},
#         ],
#         "disable_search": False,
#         # "system": "" 可选参数，输入扮演的角色
#         "enable_citation": False
#     }


def get_platform_response(message: dict) -> str:
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token()

    payload = json.dumps(message)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)["result"]


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def get_user_message(mes: str) -> dict:
    return {
        "role": "user",
        "content": mes
    }


def sent_add_platform_message(mes: str) -> dict:
    return {
        "role": "assistant",
        "content": mes
    }


# print(get_platform_response(massage))


#
# 生成教学大纲
def generate_outline(plan, level, studyStyle, communicationStyle, expressionStyle):
    # plan = "计算机"
    # level = "大学本科"
    # studyStyle = "理论型"
    # communicationStyle = "命令型"
    # expressionStyle = "严厉型"

    mes = """
    请你充当一位智能AI导师，给我列一个教学大纲。我会给你我的学习阶段和学习风格以及我想让你以怎样的沟通风格和表达风格跟我对话，教我学习。比如现在我的学习目标是如何烘烤面包，学习阶段是大学，学习风格是行动型，我希望与你的沟通风格是通俗易懂的，表达风格是鼓励的。你只需要给我返回python中字典的格式，不需要其它字描述。你应该返回类似下面的结果:
{
"课程目标":{
“描述”:"学习如何烘烤面包"
},
"课程内容":{
"1.面包烘烤基础知识":["面包的种类与特点","面包烘烤的原料与工具","面包烘烤的基本原理"],
"2.面包烘烤步骤详解":["面团制作：原料的配比、搅拌、发酵等","面团成型：各种面包的形状制作","烘烤过程：预热、放入面团、烘烤时间与温度控制","面包的出炉与冷却"]
},
"课程安排":{
"课时1":"面包烘烤基础知识",
"课时2":"面包烘烤步骤详解",
"课时3":"面包烘烤常见问题与解决方法",
"课时4":"面包的创新与变化"
},
"课程评估":{
  "描述": "通过理论测试、实践操作和成果展示等方式，对学员的学习成果进行评估，确保学员掌握所学内容并能够独立进行面包烘烤。"
},
"教学风格与沟通方式":{
  "描述": "采用通俗易懂的语言，鼓励学员积极参与和提问，营造轻松愉快的学习氛围，确保学员能够充分理解和掌握所学内容。"  
}
}
    """ + f"""同理当我想学习{plan}，学习阶段是{level}，学习风格是{studyStyle}，沟通风格是{communicationStyle}，表达风格是{expressionStyle}，
    按这个逻辑生成一份教学大纲给我，记住课程内容和课程安排要按顺序来"""
    massage = \
        {
            "messages": [
                {"role": "user", "content": mes},
            ],
            "disable_search": False,
            # "system": "" 可选参数，输入扮演的角色
            "enable_citation": False
        }
    res = get_platform_response(massage)
    res = res.replace('json', '')
    res = res.replace('```', '')
    # print(res)
    # print(json.loads(res))
    return json.loads(res)

# generate_outline()

