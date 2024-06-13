
import os
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, wait
from io import BytesIO

fastGptUrl = 'http://192.168.201.13:3000'
uploadUrl = fastGptUrl + '/api/common/file/upload'
csvTableUrl = fastGptUrl + '/api/core/dataset/collection/create/csvTable'
linkUrl = fastGptUrl + '/api/core/dataset/collection/create/link'
loginUrl = fastGptUrl + '/api/support/user/account/loginByPassword'
#appKey = 'fastgpt-lKLdemNYfLBS59Sl2phhRl9jqCkyy6z101fv56Wbhp7h6yCiM7pL'

appKey = 'fastgpt-FFQSCBb5tFZC8CGBMIGqSnmwUxSXOPMuafZrGmf34Sh2heBVUyurCOf9nq'


def batch_upload_fastgpt_data(token,parentId,datasetId,directory_path):
    files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交所有文件的上传任务
        futures = {executor.submit(upload_file, token, parentId,datasetId,file): file for file in files}
        wait(futures)

def upload_file(token,parentId,datasetId,file_path):
    headers = {
        'token': token  # 如果需要身份验证
        # 'Content-type': "multipart/form-data; charset=utf-8"
    }
    try:
        # 配置上传文件的参数
        files = {
            'file': (quote(os.path.basename(file_path)), open(file_path, 'rb')),
            'metadata': (None, '{}'),
            'bucketName': (None, 'dataset')
        }
        response = requests.post(upload_url, headers=headers, files=files)
        if response.status_code == 200:
            response_json = response.json()
            data = response_json.get('data', {})
            if data:
                print('上传文件成功---' + filename + '---fileId=' + data)
                create_fastgpt_csvTable(parentId,datasetId, data)
    except Exception as e:
        return {'error': str(e)}


def upload_fastgpt_data(token,directory_path):
    # 只处理特定类型的文件，例如CSV文件
    allowed_extensions = ['.csv']

    # 定义请求头
    headers = {
        'token': token  # 如果需要身份验证
        # 'Content-type': "multipart/form-data; charset=utf-8"
    }
    uploadFiles = []

    # 遍历目录中的所有文件
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # 检查是否为文件以及文件类型是否在允许的范围内
        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in allowed_extensions:
            # 定义要上传的文件
            files = {
                'metadata': '{}',
                'bucketName': 'dataset',
                'file': (quote(filename), open(file_path, 'rb'), 'text/csv')
            }
            data = {
                'metadata': '{}',
                'bucketName': 'dataset'
            }
            multipart_data = MultipartEncoder(fields=files)
            headers['Content-Type'] = multipart_data.content_type
            # 发送HTTP POST请求
            response = requests.post(uploadUrl, headers=headers, data = multipart_data)

            # 检查响应状态码并输出响应内容
            if response.status_code == 200:
                response_json = response.json()
                data = response_json.get('data', {})
                if data:
                    print('上传文件成功---' + filename)
                    uploadFiles.append(data)
    return uploadFiles



def upload_remote_fastgpt_data(token, file_urls):
    # 只处理特定类型的文件，例如CSV文件
    allowed_extensions = ['.csv']

    # 定义请求头
    headers = {
        'token': token  # 如果需要身份验证
    }
    #uploadFiles = []

    #
    #filename = file_url.split('?')[0].split('/')[-1]

    # 检查文件类型是否在允许的范围内

    # 从远程URL读取文件内容
    response = requests.get(file_urls)
    if response.status_code == 200:
        files = {
            'metadata': '{}',
            'bucketName': 'dataset',
            'file': ("test.csv", BytesIO(response.content), 'text/csv')
        }
        multipart_data = MultipartEncoder(fields=files)
        headers['Content-Type'] = multipart_data.content_type

        # 发送HTTP POST请求
        response = requests.post(uploadUrl, headers=headers, data=multipart_data)

        # 检查响应状态码并输出响应内容
        if response.status_code == 200:
            response_json = response.json()
            data = response_json.get('data', {})
            if data:
                print('上传文件成功---' + "")
                return data



#创建表格集合
def create_fastgpt_csvTable(parentId,datasetId,fileId):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    data = {
        'parentId': parentId,
        'datasetId': datasetId,
        'fileId': fileId
    }
    response = requests.post(csvTableUrl, data=json.dumps(data), headers=headers)
    # 检查响应状态码并输出响应内容
    if response.status_code == 200:
        print('创建成功-' + fileId)


#创建链接集合
def create_fastgpt_link(appKey,parentId,datasetId,link):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    data = {
        'parentId': parentId,
        'datasetId': datasetId,
        'link': link
    }
    response = requests.post(linkUrl, data=json.dumps(data), headers=headers)

    # 检查响应状态码并输出响应内容
    if response.status_code == 200:
        print('创建成功-' + fileId)

#创建文本集合
def create_fastgpt_file(url,appKey,parentId,datasetId,fileId):
    apiPath = '/api/core/dataset/collection/create/file'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    data = {
        'chunkSplitter': '',
        'parentId': parentId,
        'datasetId': datasetId,
        'fileId': fileId
    }
    response = requests.post(url + apiPath, data=json.dumps(data), headers=headers)

    # 检查响应状态码并输出响应内容
    if response.status_code == 200:
        print('创建集合成功-' + fileId)




def create_collection(url,appKey,collectionNames):
    apiPath = '/api/core/dataset/collection/create'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }

    for collectionName in collectionNames:
        data = {
            "datasetId": '66680ebba1d4f2f9ce06ad0b',
            "parentId": '',
            "name": collectionName,
            "type":"folder",
            "metadata":{}
        }
        response = requests.post(url + apiPath, data=json.dumps(data), headers=headers)
        # 检查响应状态码并输出响应内容
        if response.status_code == 200:
           print('创建目录成功-' + collectionName)


#666260ec90f445e5899497dc


#获取token
def fastgpt_login(username,password):
    headers = {'Content-Type': 'application/json'}
    data ={
        "username":username,
        "password":password
    }
    response = requests.post(loginUrl, data=json.dumps(data), headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
       response_json = response.json()
       token = response_json.get('data', {}).get('token', None)
       if token:
           print('Token:', token)
           return token
       else:
           print('Token not found in the response')
    else:
        print('Failed to fetch data. Status Code:', response.status_code)
        print('Response Body:', response.text)


def handler(parentId,datasetId,directory_path):
    token = fastgpt_login('root','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')

    if token is None:
        print("token 获取异常")
    else:
        fileIds = upload_remote_fastgpt_data(token,directory_path)


        create_fastgpt_csvTable(parentId,datasetId,fileIds)


def get_mongo_data(uri, database_name, collection_name, query={}):
    try:
        # 连接到 MongoDB
        client = MongoClient(uri)

        # 选择数据库
        database = client[database_name]

        # 选择集合
        collection = database[collection_name]

        # 执行查询
        results = collection.find(query)
        result_map = {}
        # 打印查询结果
        for row in results:
            print(row)
            key = row["name"]
            value = row["id"]
            result_map[key] = value

        return result_map
    except Exception as e:
        print(f"错误: {e}")

    finally:
        # 关闭 MongoDB 连接
        client.close()

if __name__ == '__main__':
    # datasetId = input("请输入datasetID：")
    # parentId = input("请输入parentID：")
    # file_path = input("请输入文件目录：")
    # fastgpturl = input("请输入fastgpt地址：")
    # appKey = input("请输入appKey：")

    datasetId = '666260ec90f445e5899497dc'
    parentId = ''
    #file_path= '/Users/jinmu/Downloads/fastgpt'
    #fileUrl = 'http://192.168.201.13:9090/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2dwdGtub3dsZWRnZS8lRTUlOUIlQkQlRTUlQUUlQjYlRTYlOTQlQkYlRTclQUQlOTYlRTglQTElQTguY3N2P1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9RTBENkNUMTkyVlhQVlVWSDZLQ0olMkYyMDI0MDYwNSUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA2MDVUMDM1NTA1WiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPWV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpoWTJObGMzTkxaWGtpT2lKRk1FUTJRMVF4T1RKV1dGQldWVlpJTmt0RFNpSXNJbVY0Y0NJNk1UY3hOell3TWpJeU1Td2ljR0Z5Wlc1MElqb2liV2x1YVc5aFpHMXBiaUo5LkhvbkpxTnIwRmJfMzRXZ0s2SnZVQWF3aEVQSGFVZ2hVOFJFZEp1TVR6ZGVrR3VLemdzemg5Z2FURVJPM2czOTlBblNXXzF6UHczX0Q4Y3pJQlB5SXR3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZ2ZXJzaW9uSWQ9bnVsbCZYLUFtei1TaWduYXR1cmU9NWIwZGE1NzQ5YjdhMDgxMmE4NWM5MmI5Yjk0MGZlZWJmM2MwYjM2NzRhODgwMTFiNWY5ZDEzYzA5OGYzZTM2Yw=='


    #handler(parentId,datasetId,fileUrl)
    cl = {
        '银行',
    '水泥建材',
    '橡胶制品',
    '专用设备',
    '电机',
    '电网设备',
    '化纤行业',
    '贸易行业',
    '房地产开发',
    '风电设备',
    '汽车整车',
    '装修建材',
    '电力行业',
    '生物制品',
    '酿酒行业',
    '玻璃玻纤',
    '通信服务',
    '钢铁行业',
    '教育',
    '电子化学品',
    '文化传媒',
    '航运港口',
    '半导体',
    '化学制药',
    '工程建设',
    '采掘行业',
    '化学原料',
    '非金属材料',
    '汽车服务',
    '公用事业',
    '农药兽药',
    '食品饮料',
    '物流行业',
    '医疗器械',
    '造纸印刷',
    '工程咨询服务',
    '电池',
    '贵金属',
    '光伏设备',
    '电子元件',
    '煤炭行业',
    '装修装饰',
    '燃气',
    '家用轻工',
    '光学光电子',
    '塑料制品',
    '能源金属',
    '航天航空',
    '仪器仪表',
    '专业服务',
    '有色金属',
    '电源设备',
    '软件开发',
    '家电行业',
    '商业百货',
    '纺织服装',
    '小金属',
    '珠宝首饰',
    '船舶制造',
    '其他',
    '房地产服务',
    '医药商业',
    '汽车零部件',
    '消费电子',
    '石油行业',
    '中药',
    '交运设备',
    '化学制品',
    '化肥行业',
    '美容护理',
    '证券',
    '通用设备',
    '工程机械',
    '多元金融',
    '保险',
    '包装材料',
    '旅游酒店',
    '通信设备',
    '环保行业',
    '互联网服务',
    '计算机设备',
    '医疗服务',
    '农牧饲渔',
    '航空机场',
    '游戏',
    '铁路公路'
    }


provinces = [
    "北京市", "天津市", "河北省", "山西省", "内蒙古自治区",
    "辽宁省", "吉林省", "黑龙江省", "上海市", "江苏省",
    "浙江省", "安徽省", "福建省", "江西省", "山东省",
    "河南省", "湖北省", "湖南省", "广东省", "广西壮族自治区",
    "海南省", "重庆市", "四川省", "贵州省", "云南省",
    "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区",
    "新疆维吾尔自治区", "台湾省", "香港特别行政区", "澳门特别行政区"
    ]
create_collection('http://192.168.201.13:3000',appKey,provinces)