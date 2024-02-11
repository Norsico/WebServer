import requests

appid = "wx2968699a71b0ec46"
secret = "c24caa833278717fc109b67987fd13cb-"
js_code = "0f11U20w3dwCd23fPh2w3K38iB21U204"
url = (f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={js_code}&grant_type"
       "=authorization_code")

response = requests.get(url)

print(response.text)
