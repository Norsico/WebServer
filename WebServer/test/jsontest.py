import json

test = "{\"allAnswer\":[\"B\",\"A\",\"A\"],\"questions\":[{\"答案\":\"B\",\"解释\":\"在JavaScript中，变量名不能以数字开头（选项A），不能是保留字（选项C中的'var'是保留字），也不能包含特殊字符（如选项D中的'#'）。因此，选项B（'variable-name'）是合法的变量名。\",\"选项\":[\"A. 1stVariable\",\"B. variable-name\",\"C. var\",\"D. #variable\"],\"题目\":\"在JavaScript中，以下哪个选项是合法的变量名？\",\"我的选项\":\"B\"},{\"答案\":\"A,B\",\"解释\":\"在JavaScript中，单行注释以'//'开始，直到行尾。多行注释以'/*'开始，以'*/'结束。因此，选项A和B都是正确的注释方式，而选项C和D都是错误的。\",\"选项\":[\"A. // 这是一个单行注释\",\"B. /* 这是一个多行注释 */\",\"C. # 这是一个单行注释\",\"D. ///* 这是一个错误的注释方式 */\"],\"题目\":\"JavaScript中的注释应该如何书写？\",\"我的选项\":\"B\"},{\"答案\":\"A\",\"解释\":\"在JavaScript中，'console.log()' 函数用于在控制台输出信息。选项A是正确的。而选项B的'print()'，选项C的'alert()'和选项D的'echo()'都不是JavaScript中的标准输出函数。\",\"选项\":[\"A. console.log('Hello, World!')\",\"B. print('Hello, World!')\",\"C. alert('Hello, World!')\",\"D. echo('Hello, World!')\"],\"题目\":\"以下哪个语句在JavaScript中会输出'Hello, World!'到控制台？\",\"我的选项\":\"C\"}],\"成绩\":33}"

data = json.loads(test)

print(data)
