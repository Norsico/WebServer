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

def calculate_score(standard_answers, your_answers):
    total_score = 0
    total_items = len(standard_answers)
    score_per_item = 100 / total_items

    for sa, ya in zip(standard_answers, your_answers):
        if sa == ya:
            total_score += score_per_item

    return total_score


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


def generate_exams(planName, courseName):
    mes = """
    请你当一个出题人，出一些选择题，并给出答案和简短的解释，返回给我的是一个json，比如出2道关于的是"学习JavaScript"任务中的"课时2. 条件语句、循环语句与函数"。成绩一直是0就可以了。你的结果应该是:{
"questions":[
 {  
        "题目": "在JavaScript中，以下哪个关键字用于声明一个函数？",  
        "选项": [  
            "A. var",  
            "B. function",  
            "C. let",  
            "D. const"  
        ],  
        "答案": "B",  
        "解释": "在JavaScript中，'function' 关键字用于声明一个函数。"  
    },  
    {  
        "题目": "以下哪个语句会创建一个无限循环？",  
        "选项": [  
            "A. for (let i = 0; i < 10; i++) {}",  
            "B. while (true) {}",  
            "C. do {} while (false);",  
            "D. for (let i = 0; i > 0; i--) {}"  
        ],  
        "答案": "B",  
        "解释": "'while (true) {}' 会一直执行，因为没有条件可以使循环终止，所以它是一个无限循环。"  
    },  
],"allAnswer":["B","B"],"成绩":  0
}现在请你3道在任务""" + f"{planName}中的{courseName}"
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
    return json.loads(res)

# generate_exams("学习JavaScript", "课时2. 条件语句、循环语句与函数")


def generate_details(courseName, details):
    # courseName = "课时1. JavaScript概述与基础语法"
    # details = "switch多分支选择语句"
    mes = "我在学" + f"{courseName}，这里面的{details}我不太懂，简要介绍，简短一点"
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
    # print(res)
    # print(json.loads(res))
    return res


# generate_details()


def generate_knowledgePoint(planName, courseName, style):
    # planName = "学java"
    # courseName = "课时7.JDBC数据库编程实践"
    # style = "采用正式的教学风格，注重理论与实践相结合，鼓励学员通过直觉理解编程概念，培养编程思维。通过清晰的逻辑和严谨的表达，帮助学员更好地掌握Java编程知识。"
    mes = """
请你充当一个AI老师，比如我给你一个:假如我有一个计划"学习linux"，我要学习里面的"课时2.常用命令"，学习方式是"采用通俗易懂、幽默风趣的语言，结合丰富的实例和实战演练，让学员在轻松愉快的氛围中快速掌握Linux操作系统的核心知识和技能。"，你的回答只用返回一个json:{  
  "title": "课时2.常用命令",  
  "description": "深入探索Linux的常用命令，涵盖文件操作、进程管理、网络配置等核心功能。",  
  "learningObjectives": [  
    "掌握Linux系统中常用的基本命令及其功能",  
    "能够独立使用命令进行文件和目录管理",  
    "理解进程管理命令，并能够进行简单的进程控制",  
    "熟悉系统信息和网络相关命令，解决实际问题"  
  ],  
  "content": {  
    "conceptExplanation": {  
      "常用命令": "Linux系统中的基本命令，用于执行各种任务，如文件操作、进程管理、网络配置等。",  
      "命令语法": "每个命令都有其特定的语法结构，包括命令名、选项和参数。",  
      "命令选项": "命令选项用于修改命令的默认行为，以满足特定的需求。"  
    },  
    "details": [  
      {  
        "name": "第1节. 文件操作命令",  
        "example": [  
          "ls -l：以长格式列出当前目录下的文件和目录",  
          "cd /home/user：切换到/home/user目录",  
          "pwd：显示当前工作目录的路径",  
          "cp file1 file2：复制file1到file2",  
          "mv file1 dir/：将file1移动到dir/目录下",  
          "rm -r dir：递归删除dir目录及其内容" 
        ]  
      },  
      {  
        "name": "第2节. 进程管理命令",  
        "example": [  
          "ps aux：查看当前系统上的所有进程",  
          "top：实时显示系统中各个进程的状态",  
          "kill -9 PID：强制终止PID指定的进程"  
        ]  
      },  
      {  
        "name": "第3节. 网络相关命令",  
        "example": [  
          "ifconfig：查看和配置网络接口",  
          "ping www.google.com：测试与www.google.com的网络连通性",  
          "netstat：查看网络连接、路由表、接口统计等信息"  
        ]  
      }  
    ]  
  },  
  "additionalResources": [  
    "实战模拟资源：如在线实验平台，允许学生亲手操作Linux命令，加深理解",  
    "通俗易懂的学习资料：如Linux命令速查手册，用简洁明了的语言解释命令用法",  
    "幽默风格的教学视频：如B站上有轻松幽默讲解Linux命令的视频"  
  ]  
} 并且这个json的键不能改变！""" + f"""现在假如我的计划是"{planName}"，我要学习里面的"{courseName}"，学习方式是{style}"""
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


# generate_knowledgePoint()


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
    "计算机基础知识": [
        "*计算机基础知识*",  
        "计算机的发展历程与分类",  
        "计算机硬件与软件的基本概念",  
        "计算机中的数据表示与运算"  
    ],  
    "操作系统": [  
        "*操作系统*",
        "操作系统的基本原理与功能",  
        "常见操作系统的使用与管理",  
        "进程管理、内存管理、文件管理等核心概念"  
    ],  
    "编程语言": [  
        "*编程语言*",
        "编程语言的基本概念与分类",  
        "Python/Java/C++等主流编程语言的学习与实践",  
        "算法与数据结构的基本概念与应用"  
    ],  
    "网络技术": [  
        "*网络技术*",
        "计算机网络的基本原理与分类",  
        "局域网、广域网与互联网的基本概念",  
        "TCP/IP协议族与HTTP协议等核心概念"  
    ]  
  },  
  "课程安排": {  
    "课时1": "课时1.计算机基础知识",  
    "课时2": "课时2.操作系统",  
    "课时3": "课时3.编程语言 - Python/Java/C++入门",  
    "课时4": "课时4.算法与数据结构基础",  
    "课时5": "课时5.计算机网络基础",  
    "课时6": "课时6.编程语言进阶 - Python/Java/C++深入学习",  
    "课时7": "课时7.项目实践 - 小型程序设计",  
    "课时8": "课时8.课程总结与未来展望"  
  },  
  "课程评估": {  
    "描述": "通过理论测试、编程实践和项目考核等方式，对学员的学习成果进行评估，确保学员掌握所学内容并能够独立进行编程实践。"  
  },  
  "教学风格与沟通方式": {  
    "描述": "采用通俗易懂的语言，注重实践与应用，鼓励学员积极参与和提问，营造轻松愉快的学习氛围。通过实例和案例，帮助学员更好地理解和掌握计算机知识。"  
  }  
}
    """ + f"""同理当我想学习{plan}，学习阶段是{level}，学习风格是{studyStyle}，沟通风格是{communicationStyle}，表达风格是{expressionStyle}，
    按这个逻辑生成一份教学大纲给我"""
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
