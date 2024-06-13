import requests

"""添加请求头：header"""

headers = {'Cookie':'BIDUPSID=ED00CAE061275E563D039479F0F2D1A0; PSTM=1648197684; BDUSS=VRSmtKa09naURQaEpSZVlYVk1SbHlVbGNrclU2ODBOflNDMXZpd1N1YmplNjVpSVFBQUFBJCQAAAAAAAAAAAEAAAAQgzgvtPO57WFzZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOPuhmLj7oZiN2; BDUSS_BFESS=VRSmtKa09naURQaEpSZVlYVk1SbHlVbGNrclU2ODBOflNDMXZpd1N1YmplNjVpSVFBQUFBJCQAAAAAAAAAAAEAAAAQgzgvtPO57WFzZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOPuhmLj7oZiN2; jsdk-uuid=055e03f4-2908-4ad5-898d-7add76057737; BAIDUID_BFESS=BDB908088D33972A709CCB27F11AD940:FG=1; BD_UPN=123253; BA_HECTOR=a40l0580858ka02h21a12h2o1ii4hep1o; ZFY=DtPhq9yrBltyDWY7L2:BEzXPK:AQZoLCwvRhIY6IT:BMzE:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598'
           }

"""带请求参数"""
params = {'wd':'python'}

"""代理设置"""
proxies = {'http':'http://127.0.0.1:9743',
           'https':'https://127.0.0.1:9742'}

"""SSL证书验证"""
response = requests.get('https://www.12306.cn',verify=False)


"""超时设置"""
from requests.exceptions import ReadTimeout
try:
    response = requests.get("http://httpbin.org/get", timeout = 0.5)
    print(response.status_code)
except ReadTimeout:
    print('timeout')

"""认证设置"""
from requests.auth import HTTPBasicAuth
response = requests.get("http://120.27.34.24:9001/",auth=HTTPBasicAuth("user","123"))
print(response.status_code)


"""post请求"""

import requests
import json

host = 'http://httpbin.org/'
endpoint = 'post'
url = ''.join([host,endpoint])

"""带数据的post"""
data = {'key1':'value1','key2':'value2'}
response = requests.post(url,data=data)
print(response.status_code)
print(response.text)

"""带headers的post"""
headers = {'User-Agent':'test request headers'}
response = requests.post(url,headers=headers)
print(response.status_code)
print(response.text)

"""带json的post"""
data = {
    'sites':[
        {'name':'test','url':'www.test.com'},
        {'name':'google','url':'www.google.com'},
        {'name':'weibo','url':'www.weibo.com'}
    ]
}
response = requests.post(url,json=data)
print(response.status_code)
print(response.text)

"""带参数的post"""
params = {'key1':'params1','key2':'params'}
response = requests.post(url,params=params)
print(response.status_code)
print(response.text)

"""文件上传"""
files = {'file':open('fisrtgetfile.txt','rb')}
response = requests.post(url,files=files)
print(response.status_code)
print(response.text)

"""put请求"""
import requests
import json

url = 'http://127.0.0.1:8080'
header = {'Content-Type':'application/json'}
param = {'myObjectField':'hello'}
payload = json.dumps(param)

response = requests.put(url,data=payload,headers=headers)

#设置中文乱码
response.encoding = 'utf-8'
html = response.text

print(html)








