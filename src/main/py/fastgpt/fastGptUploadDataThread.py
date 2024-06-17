import os
import json
import time

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib.parse import quote
from io import BytesIO
import pymysql
from urllib.parse import urlparse
import concurrent.futures

fastGptUrl = 'http://192.168.201.13:3000'
uploadUrl = fastGptUrl + '/api/common/file/upload'
csvTableUrl = fastGptUrl + '/api/core/dataset/collection/create/csvTable'
linkUrl = fastGptUrl + '/api/core/dataset/collection/create/link'
fileUrl = fastGptUrl + '/api/core/dataset/collection/create/file'
loginUrl = fastGptUrl + '/api/support/user/account/loginByPassword'
collectionUrl = fastGptUrl + '/api/core/dataset/collection/create'
datasetUrl = fastGptUrl + '/api/core/dataset/create'
collectionListUrl = fastGptUrl + '/api/core/dataset/collection/list'
appKey = 'fastgpt-9TnYVdHG5RJ8fsQirqFwPpIHkGKVsezUJDqhW3WeHQqUBVNotGvGREhMbUFoz'
fast_username = 'root'
fast_password= '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'

update_query = "UPDATE stg_model.report_base SET report_status = %s WHERE id = %s"

parentId = ''
datasetId ='66680ea4a1d4f2f9ce06acd7'
token = ''
collection_map = {}

def read_mysql_data(host, database, user, password, port, query):
    try:
        # 连接到 MySQL 数据库
        connection = pymysql.connect(
            host=host,
            port=port,  # 指定自定义端口
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()

        if records is None:
            global flag
            flag = False
        batches = list(split_records_into_batches(records, 500))

        # 使用 ThreadPoolExecutor 进行多线程处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # 提交任务
            futures = [executor.submit(process_record, list(record), collection_map, token, parentId, datasetId, host,port,user,password,database) for record in batches]
            # 等待所有任务完成
            concurrent.futures.wait(futures)
    except pymysql.MySQLError as e:
        print(f"错误: {e}")
    finally:
        # 关闭数据库连接
        if connection:
            cursor.close()
            connection.close()
            print("MySQL 数据库连接已关闭")

def update_mysql_data(connection, update_params):
    try:
        cursor = connection.cursor()
        cursor.execute(update_query, update_params)
        # 提交事务
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"错误: {e}")
        connection.rollback()  # 在出现错误时回滚事务

def split_records_into_batches(records, batch_size):
    # 将记录分批
    for i in range(0, len(records), batch_size):
        yield records[i:i + batch_size]

# 定义处理单个记录的函数
def process_record(records, collection_map, token, parentId, datasetId, host,port,user,password,database):
    t=time.time()
    try:
        connection = pymysql.connect(
            host=host,
            port=port,  # 指定自定义端口
            user=user,
            password=password,
            database=database
        )
        for record in records:
                id = record[0]
                industry = record[9]
                url = record[25]
                cid = collection_map.get(industry)
                if cid is None:
                    collection_id = get_collection_list(parentId, datasetId, industry)
                    if collection_id is None:
                        collection_id = create_collection(industry)
                    collection_map[industry] = collection_id
                fileId = upload_remote_fastgpt_data(token, url)
                upload_status = create_fastgpt_file(collection_map.get(industry), datasetId, fileId, '')
                if upload_status:
                    update_params = ('1', id)
                    update_mysql_data(connection, update_params)
                    print(f"更新数据库成功---id---{id}")
    except Exception as e:
        print(f'处理异常==>{e}==>record==>{record}')
    finally:
        if connection:
            connection.close()
            print("MySQL 数据库连接已关闭")
    print(f"处理耗时==>{time.time()-t}")

#读取远程地址文件上传到fastgpt
def upload_remote_fastgpt_data(token, file_url):
    headers = {
        'token': token  # 如果需要身份验证
    }
    # 解析 URL
    parsed_url = urlparse(file_url)

    # 获取文件名（带后缀）
    file_name = os.path.basename(parsed_url.path)
    # 获取文件类型
    file_type = os.path.splitext(file_name)[1][1:]  # 去除文件后缀的点号

    # 从远程URL读取文件内容
    response = requests.get(file_url)
    if response.status_code == 200:
        # 确定文件类型
        if file_type.lower() == 'pdf':
            file_mime_type = 'application/pdf'
        else:
            file_mime_type = 'text/' + file_type
        files = {
            'metadata': '{}',
            'bucketName': 'dataset',
            'file': (file_name, BytesIO(response.content), file_mime_type)
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
                print('上传文件成功---' + file_url)
                return data


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
        response = requests.post(uploadUrl, headers=headers, files=files)
        if response.status_code == 200:
            response_json = response.json()
            data = response_json.get('data', {})
            if data:
                print('上传文件成功---' + file_path + '---fileId=' + data)
                create_fastgpt_csvTable(parentId,datasetId, data)
    except Exception as e:
        return {'error': str(e)}


def upload_fastgpt_data(token,directory_path):
    # 只处理特定类型的文件，例如CSV文件
    allowed_extensions = ['.csv','.pdf','.txt','.word']

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
        print('创建链接成功')

#创建文本集合
def create_fastgpt_file(parentId,datasetId,fileId,chunkSplitter):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    data = {
        'parentId': parentId,
        'datasetId': datasetId,
        'fileId': fileId
    }
    if chunkSplitter:
        data['chunkSplitter'] = chunkSplitter

    response = requests.post(fileUrl, data=json.dumps(data), headers=headers)

    # 检查响应状态码并输出响应内容
    if response.status_code == 200:
        print('创建文本集合成功-' + fileId)
        return True
    else:
        print("创建文本集合失败-" + fileId)
        return False


# 获取集合目录list
def get_collection_list(parentId,datasetId,text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    data = {
        'pageNum': 1,
        'pageSize': 20,
        'parentId': parentId,
        'datasetId': datasetId,
        'searchText': text
    }
    response = requests.post(collectionListUrl, data=json.dumps(data), headers=headers)
    # 检查响应状态码并输出响应内容
    if response.status_code == 200:
        response_json = response.json()
        data_array = response_json['data']['data']
        if data_array:
            _id = data_array[0]["_id"]
            print("查询获取的集合id:", _id)
            return _id
    else:
        return None


#创建空集合目录
def create_collection(collectionName):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    data = {
        "datasetId": datasetId,
        "parentId": parentId,
        "name": collectionName,
        "type":"folder",
        "metadata":{}
    }
    response = requests.post(collectionUrl, data=json.dumps(data), headers=headers)
    # 检查响应状态码并输出响应内容
    if response.status_code == 200:
        print('创建目录成功--' + collectionName)
        response_json = response.json()
        data = response_json.get('data', {})
        if data:
            return data


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


#批量创建知识库
def batch_create_dataset(parentId,datasetNames):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    for datasetName in datasetNames:
        data = {
            'agentModel':'moonshot-v1-128k',
            'avatar': '/icon/logo.svg',
            'name' : '企业基础数据-' + datasetName,
            'intro': '',
            'parentId': parentId,
            'type': 'dataset',
            'vectorModel': 'm3e'
        }
        response = requests.post(datasetUrl,data = json.dumps(data), headers=headers)
        # 检查响应状态码并输出响应内容
        if response.status_code == 200:
           print('创建知识库成功--' + datasetName)




if __name__ == '__main__':
    # # 示例使用
    # host = '192.168.201.14'
    # database = 'stg_model'
    # port = 3305
    # user = 'root'
    # password = 'Gysj_2024'
    # query = 'SELECT * FROM stg_model.report_base where report_status = \'0\' limit 100'
    #
    # token = fastgpt_login(fast_username,fast_password)
    # read_mysql_data(host,database,user,password,port,query)

    flag = True

    while flag:
        # 示例使用
        host = '192.168.201.14'
        database = 'stg_model'
        port = 3305
        user = 'root'
        password = 'Gysj_2024'
        query = 'SELECT * FROM stg_model.report_base where report_status = \'0\' limit 5000'

        token = fastgpt_login(fast_username,fast_password)
        read_mysql_data(host,database,user,password,port,query)

    print("全部执行完成")
