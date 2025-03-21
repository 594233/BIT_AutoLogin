import requests
import json
import re
import execjs
import socket
# 分别填入学号（studentID）、密码（password）
studentID = ""
password = ""


ipv4s = socket.gethostbyname_ex(socket.gethostname())[2]
print(ipv4s)
# 需要维护ip，main_login内的ip
def strtodict(str):
    comment = re.compile(r"\(.*\)", re.DOTALL)
    match_result = comment.findall(str)
    if match_result:
        json_str = match_result[0][1:-1]
        # 解析JSON字符串为字典
        data_dict = json.loads(json_str)
    else:
        data_dict = {}
        print("没有匹配到预期的JSON部分内容，请检查输入内容是否符合格式要求。")
    return data_dict

def get_call():
    headers = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://10.0.0.55/srun_portal_pc?ac_id=43&srun_wait=1&theme=bit",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    cookies = {
        "lang": "zh-CN",
    }
    url = "http://10.0.0.55/cgi-bin/get_challenge"
    params = {
        "callback": "jQuery",
        "username": studentID,
        "ip": ipv4s,
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)
    return get_param(response.text)

def get_param(response_text):
    response_dict = strtodict(response_text)
    response_dict["studentID"] = studentID
    response_dict["password"] = password
    print("Call1:" + str(response_dict))
    file = 'main_login.js'
    ctx = execjs.compile(open(file).read())
    print('in_js')
    param = json.loads(ctx.call("login",json.dumps(response_dict)))
    print("params:" + str(param))
    return param

def get_login(params):
    headers = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://10.0.0.55/srun_portal_pc?ac_id=43&srun_wait=1&theme=bit",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    cookies = {
        "lang": "zh-CN",
    }
    url = "http://10.0.0.55/cgi-bin/srun_portal"
    params["callback"] = "jQuery"

    response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)
    response_dict = strtodict(response.text)
    print("Call2:" + str(response_dict))
    print(response_dict["res"])
    if "suc_msg" in response_dict:
        print(response_dict["suc_msg"])
    else:
        print(response_dict["error_msg"])

param = get_call()
get_login(param)






