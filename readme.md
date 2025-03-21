# 北京理工大学校园网自动认证登录
## 原理讲解
[跳转至使用说明](#jump)
### 认证请求流程
有线网、无线网连接后即分配ip，只有认证后才有网络，很久不登录ip可能会重新分配，所以需要动态ip设置，使用socket库确定ip地址  
- 网页有重定向(`get_call()`实现)，首先向某个网址发送请求得到token(`chanllenge`)
- 随后将账号、密码、token等信息加密成`param`(`get_param()`实现)
- 随后带着`param`进行登录验证(`get_login()`实现)  

### 得到token  
发送请求包含动态的ip，返回结果包含加密参数`challenge`   
使用re模块编译一个正则表达式，匹配括号里的所有内容  
第一个括号里包含了json格式的`challenge`信息，切片取值，并加载储存为字典格式
```Python
# request返回值为：jQuery***_***(json{***})，需要匹配括号中的json片段
r"\(.*\)"  
# \( 和 \)：这两个符号是转义字符，用于匹配实际的括号 ( 和 )。
# .*：  .表示匹配任意字符（默认不包括换行符）， *表示匹配前面的字符零次或多次。因此，.* 会匹配括号内的任意内容。
# 得到结果：
response.text = '{"challenge":"", "client_ip":"","ecode":,"error":"","error_msg":"","expire":","online_ip":"", "res":"","srun_ver":"","st":}'
```
### 加密`param`  
逆向网站，得到`challenge`的加密JS代码，将所有混淆的函数参数补环境  
JS中使用`JSON.parse()`，将json转换为JS对象
对校园网密码进行了加盐的md5加密
``` JavaScrip
hmd5 = md5(data.password, token) 
```
param加密了`chksum`参数
``` JavaScrip
    var params = {
        action: "login",
        username: username,
        password: data.password,
        ac_id: data.ac_id,
        ip: response.client_ip,
        chksum: chk(chkstr),
        info: i,
        n: "200",
        type: "1",
        os: "windows 10",
        name: "windows",
        double_stack: "0",
        ignore: "2",
        // cas_account: data.cas_account,
        // cas_password: data.cas_password
    }
```
`JSON.stringify()`将JS对象封装为json传回python  
使用PyExecJs调用JS
```Python
ctx = execjs.compile(open(file).read())
# 将JS加密代码解码为python
# JS里不能有export函数，用Call传参，不要用eval()，调用ctx-js文件中的login函数，并传入参数
param = json.loads(ctx.call("login",json.dumps(response_dict)))
# JS代码中不能出现的互相文件间的调用，否则报错
```
### 认证登录
最后向定向后的网页提交`dict-params`（`get_login()`），打印`["suc_msg"]`查看登录状态  

### 注意事项
可能的报错  
- `ImportError: urllib3 v2.0 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.1.0j 20 Nov 2018'. See: https://github.com/urllib3/urllib3/issues/2168`  
[参考解决方案](https://blog.csdn.net/BetrayFree/article/details/133922849)

## 使用方法 <span id="jump"></span>
### 将项目拉取到本地
直接将代码下载到本地  
`main.py`: 进行网络请求，注意输入账号密码登录  
`main_login.js`: 负责参数的加密  
`requirements.txt`: 依赖项
### 配置所用库（requirements.txt）


### 设置windows定时任务
[参考](https://blog.csdn.net/xc_zhou/article/details/107418874#:~:text=%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95%E6%98%AF%EF%BC%9A%E4%BD%BF%E7%94%A8windows%20%E7%9A%84%E2%80%9C%E4%BB%BB%E5%8A%A1%E8%AE%A1%E5%88%92%E7%A8%8B%E5%BA%8F%E2%80%9D%20%E7%AC%AC1%E6%AD%A5%EF%BC%9A%E5%9C%A8%20%E8%AE%A1%E7%AE%97%E5%99%A8%E5%8F%B3%E5%87%BB%20--%3E%20%E9%80%89%E6%8B%A9%E7%AE%A1%E7%90%86%20%E8%BF%9B%E5%85%A5%E5%A6%82%E4%B8%8B%E7%95%8C%E9%9D%A2%EF%BC%9A%20%E7%AC%AC2%E6%AD%A5%EF%BC%9A%E9%80%89%E6%8B%A9,%E6%88%96%E8%80%85%20%E2%80%9C%E5%88%9B%E5%BB%BA%E4%BB%BB%E5%8A%A1%E2%80%9D%EF%BC%8C%E8%BF%99%E9%87%8C%E6%88%91%E7%82%B9%E5%87%BB%E5%88%9B%E5%BB%BA%E4%BB%BB%E5%8A%A1%EF%BC%8C%E8%BF%9B%E5%85%A5%E5%A6%82%E4%B8%8B%E7%95%8C%E9%9D%A2%20%E7%AC%AC3%E6%AD%A5%EF%BC%9A%E9%80%89%E6%8B%A9%20%E8%A7%A6%E5%8F%91%E5%99%A8%EF%BC%8C%E7%84%B6%E5%90%8E%E6%96%B0%E5%BB%BA%E8%A7%A6%E5%8F%91%E5%99%A8%20%E8%AE%BE%E7%BD%AE%E9%9C%80%E8%A6%81%E8%A7%A6%E5%8F%91%E7%9A%84%E6%97%B6%E9%97%B4%20%E7%AC%AC4%E6%AD%A5%EF%BC%9A%E5%88%9B%E5%BB%BA%E4%BB%BB%E5%8A%A1%EF%BC%8C%E7%82%B9%E5%87%BB%E6%93%8D%E4%BD%9C%EF%BC%8C%E7%82%B9%E5%87%BB%E6%96%B0%E5%BB%BA%20%E7%A8%8B%E5%BA%8F%E6%88%96%E8%84%9A%E6%9C%AC%EF%BC%9A%E5%A1%AB%E5%86%99%E5%8F%AF%E6%89%A7%E8%A1%8C%E7%9A%84%E6%96%87%E4%BB%B6%E8%B7%AF%E5%BE%84%20%E8%BF%99%E9%87%8C%E7%9A%84%E5%9B%BE%E7%89%87%E4%BB%85%E4%BE%9B%E4%B8%8A%E9%9D%A2%E5%A1%AB%E5%86%99%E5%8F%82%E9%98%85)
