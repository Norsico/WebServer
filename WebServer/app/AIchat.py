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


# 生成教学大纲
def generate_outline(plan, level, studyStyle, communicationStyle, expressionStyle):
    # plan = "计算机"
    # level = "大学本科"
    # studyStyle = "理论型"
    # communicationStyle = "命令型"
    # expressionStyle = "严厉型"

    mes = """
    请你充当一位智能AI导师，给我列一个教学大纲。我会给你我的学习阶段和学习风格以及我想让你以怎样的沟通风格和表达风格跟我对话，教我学习。比如现在我的学习目标是学习计算机，学习阶段是大学，学习风格是行动型，我希望与你的沟通风格是通俗易懂的，表达风格是鼓励的。你只需要给我返回python中字典的格式，不需要其它字描述。你应该返回类似下面的结果:
{  
  "课程目标": {  
    "描述": "让学员掌握计算机的基本原理、操作系统、编程语言和网络技术等基础知识，培养学员的计算思维能力和编程实践能力，为学员从事计算机相关领域的工作和研究打下基础。"  
  },  
  "课程内容": {  
    "1.计算机基础知识": [  
      "计算机的发展历程与分类",  
      "计算机硬件与软件的基本概念",  
      "计算机中的数据表示与运算"  
    ],  
    "2.操作系统": [  
      "操作系统的基本原理与功能",  
      "常见操作系统的使用与管理",  
      "进程管理、内存管理、文件管理等核心概念"  
    ],  
    "3.编程语言": [  
      "编程语言的基本概念与分类",  
      "Python/Java/C++等主流编程语言的学习与实践",  
      "算法与数据结构的基本概念与应用"  
    ],  
    "4.网络技术": [  
      "计算机网络的基本原理与分类",  
      "局域网、广域网与互联网的基本概念",  
      "TCP/IP协议族与HTTP协议等核心概念"  
    ]  
  },  
  "课程安排": {  
    "课时1": "计算机基础知识",  
    "课时2": "操作系统",  
    "课时3": "编程语言 - Python/Java/C++入门",  
    "课时4": "算法与数据结构基础",  
    "课时5": "计算机网络基础",  
    "课时6": "编程语言进阶 - Python/Java/C++深入学习",  
    "课时7": "项目实践 - 小型程序设计",  
    "课时8": "课程总结与未来展望"  
  },  
  "课程评估": {  
    "描述": "通过理论测试、编程实践和项目考核等方式，对学员的学习成果进行评估，确保学员掌握所学内容并能够独立进行编程实践。"  
  },  
  "教学风格与沟通方式": {  
    "描述": "采用通俗易懂的语言，注重实践与应用，鼓励学员积极参与和提问，营造轻松愉快的学习氛围。通过实例和案例，帮助学员更好地理解和掌握计算机知识。"  
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
