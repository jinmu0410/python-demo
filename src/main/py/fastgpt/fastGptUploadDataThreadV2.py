import os
import json
import time
from typing import List, Dict, Any

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
insertUtl = fastGptUrl + '/api/core/dataset/data/insertData'
pushUrl = fastGptUrl + '/api/core/dataset/data/pushData'

appKey = 'fastgpt-9TnYVdHG5RJ8fsQirqFwPpIHkGKVsezUJDqhW3WeHQqUBVNotGvGREhMbUFoz'
fast_username = 'root'
fast_password = '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'

update_query = "UPDATE stg_model.stg_company_basic_info SET handle_status = %s WHERE id = %s"

batch_update_query = "UPDATE stg_model.stg_company_basic_info SET handle_status = %s WHERE id in %s"

parentId = ''
datasetId = '66680ebba1d4f2f9ce06ad0b'
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
        print("执行查询" + query)
        cursor.execute(query)
        records = cursor.fetchall()

        if records is None:
            global flag
            flag = False
        batches = list(split_records_into_batches(records, 200))
        # for record in batches:
        #     process_record_list(list(record), collection_map, token, parentId, datasetId, host, port, user, password, database)
        # 使用 ThreadPoolExecutor 进行多线程处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # 提交任务
            futures = [executor.submit(
                process_record_list,
                list(record), collection_map, token, parentId, datasetId, host, port, user, password, database
            ) for record in batches]
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


def read_mysql_data_v1(host, database, user, password, port, query):
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
        print("执行查询" + query)
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except pymysql.MySQLError as e:
        print(f": {e}")
    finally:
        # 关闭数据库连接
        if connection:
            cursor.close()
            connection.close()
            print("MySQL 数据库连接已关闭")


def mid_process(records, token, parentId, datasetId, host, port, user, password, database):
    if records is None:
        global flag
        flag = False
    batches = list(split_records_into_batches(records, 200))
    #
    process_record_list(list(batches[0]), collection_map, token, parentId, datasetId, host, port, user, password,
                        database)
    batches.pop(0)
    # 使用 ThreadPoolExecutor 进行多线程处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # 提交任务
        futures = [executor.submit(
            process_record_list,
            list(record), collection_map, token, parentId, datasetId, host, port, user, password, database
        ) for record in batches]
        # 等待所有任务完成
        concurrent.futures.wait(futures)


def update_mysql_data(connection, update_params):
    try:
        cursor = connection.cursor()
        cursor.execute(update_query, update_params)
        # 提交事务
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"错误: {e}")
        connection.rollback()  # 在出现错误时回滚事务


def update_mysql_data_batch(connection, update_params):
    try:
        cursor = connection.cursor()
        update_sql = batch_update_query % update_params
        # print(update_sql)
        cursor.execute(update_sql)
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
def process_record(records, collection_map, token, parentId, datasetId, host, port, user, password, database):
    t = time.time()
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
            province = record[29].split(":")[1]
            city = record[30].split(":")[1]
            cid = collection_map.get(province)
            sub_cid = collection_map.get(city)
            # 不要id  删掉
            record_list = list(record)
            del record_list[0]
            record = tuple(record_list)

            # 创建集合：手动集合
            if cid is None:
                # 省
                tmp_map = get_collection_list(parentId, datasetId, province)
                collection_id = ''
                parent_id = ''
                if tmp_map is None:
                    # 省没有，则创建目录集合
                    collection_id = create_collection(parent_id, province, 'folder')
                    # 新建省目录后，该集合id就是目录下手动集合的父id
                    parent_id = collection_id
                else:
                    collection_id = tmp_map.get("_id")
                    parent_id = collection_id  # tmp_map.get("parentId")
                collection_map[province] = collection_id
                if sub_cid is None:
                    # 市
                    sub_tmp_map = get_collection_list(parent_id, datasetId, city)
                    if sub_tmp_map is None:
                        # 没有则创建新的集合
                        sub_collection_id = create_collection(parent_id, city, 'virtual')
                    else:
                        sub_collection_id = sub_tmp_map.get("_id")
                    collection_map[city] = sub_collection_id
            # 省存在了
            else:
                tmp_map = get_collection_list(parentId, datasetId, province)
                parent_id = tmp_map.get("_id")
                # 把省的id拿过来作为父id去获取/创建市id
                if sub_cid is None:
                    # 市
                    sub_tmp_map = get_collection_list(parent_id, datasetId, city)
                    if sub_tmp_map is None:
                        # 没有则创建新的集合
                        sub_collection_id = create_collection(parent_id, city, 'virtual')
                    else:
                        sub_collection_id = sub_tmp_map.get("_id")
                    collection_map[city] = sub_collection_id

            # 上传数据到fastGpt
            fina_collection_id = collection_map.get(city) if collection_map.get(city) else collection_map.get(province)
            upload_status = insert_data(fina_collection_id, ','.join(str(i) for i in record), "")
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
    print(f"处理耗时==>{time.time() - t}")


# 批量处理
def process_record_list(records, collection_map, token, parentId, datasetId, host, port, user, password, database):
    t = time.time()
    try:
        connection = pymysql.connect(
            host=host,
            port=port,  # 指定自定义端口
            user=user,
            password=password,
            database=database
        )

        # records属于同一个省同一个市
        first_record = records[0]
        # id = first_record[0]
        province = first_record[29].split(":")[1]
        city = first_record[30].split(":")[1]
        if province == city:
            city = city + '_virtual'
        cid = collection_map.get(province)
        sub_cid = collection_map.get(city)
        # # 不要id  删掉
        # record_list = list(first_record)
        # del record_list[0]
        # first_record = tuple(record_list)

        # 创建集合：手动集合
        if cid is None:
            # 省
            tmp_map = get_collection_list(parentId, datasetId, province)
            collection_id = ''
            parent_id = ''
            if tmp_map is None:
                # 省没有，则创建目录集合
                collection_id = create_collection(parent_id, province, 'folder')
                # 新建省目录后，该集合id就是目录下手动集合的父id
                parent_id = collection_id
            else:
                collection_id = tmp_map.get("_id")
                parent_id = collection_id  # tmp_map.get("parentId")
            collection_map[province] = collection_id
            if sub_cid is None:
                # 市
                sub_tmp_map = get_collection_list(parent_id, datasetId, city)
                if sub_tmp_map is None:
                    # 没有则创建新的集合
                    sub_collection_id = create_collection(parent_id, city, 'virtual')
                else:
                    sub_collection_id = sub_tmp_map.get("_id")
                collection_map[city] = sub_collection_id
        # 省存在了
        else:
            tmp_map = get_collection_list(parentId, datasetId, province)
            parent_id = tmp_map.get("_id")
            # 把省的id拿过来作为父id去获取/创建市id
            if sub_cid is None:
                # 市
                sub_tmp_map = get_collection_list(parent_id, datasetId, city)
                if sub_tmp_map is None:
                    # 没有则创建新的集合
                    sub_collection_id = create_collection(parent_id, city, 'virtual')
                else:
                    sub_collection_id = sub_tmp_map.get("_id")
                collection_map[city] = sub_collection_id

        # 集合准备完毕
        # 往对应的市集合下插入数据
        fina_collection_id = collection_map.get(city)
        fina_record_list = []
        id_list = []
        # 记录处理
        for ele in records:
            record_list = list(ele)
            id_list.append(record_list[0])
            del record_list[0]
            new_list = tuple(record_list)
            fina_record_list.append(','.join(str(i) for i in new_list))

        # 批量插入
        upload_status = push_data(fina_collection_id, "chunk", fina_record_list)
        if upload_status:
            # for id in id_list:
            sub_str = '(' + ','.join('\'' + str(i) + '\'' for i in id_list) + ')'
            update_params: tuple[str, str] = ('1', sub_str)

            update_mysql_data_batch(connection, update_params)
            print(f"批量更新数据库成功---id---")
            # print(f"批量更新数据库成功---id---{sub_str}")

    except Exception as e:
        print(f'处理异常==>{e}==>record==>{records}')
    finally:
        if connection:
            connection.close()
            print("MySQL 数据库连接已关闭")
    print(f"处理耗时==>{time.time() - t}")


# 读取远程地址文件上传到fastgpt
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


def upload_file(token, parentId, datasetId, file_path):
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
                create_fastgpt_csvTable(parentId, datasetId, data)
    except Exception as e:
        return {'error': str(e)}


def upload_fastgpt_data(token, directory_path):
    # 只处理特定类型的文件，例如CSV文件
    allowed_extensions = ['.csv', '.pdf', '.txt', '.word']

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
            response = requests.post(uploadUrl, headers=headers, data=multipart_data)

            # 检查响应状态码并输出响应内容
            if response.status_code == 200:
                response_json = response.json()
                data = response_json.get('data', {})
                if data:
                    print('上传文件成功---' + filename)
                    uploadFiles.append(data)
    return uploadFiles


# 创建表格集合
def create_fastgpt_csvTable(parentId, datasetId, fileId):
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


# 创建链接集合
def create_fastgpt_link(appKey, parentId, datasetId, link):
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


# 创建文本集合
def create_fastgpt_file(parentId, datasetId, fileId, chunkSplitter):
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
def get_collection_list(parentId, datasetId, text):
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
        collect_info_map = {}
        if data_array:
            _id = data_array[0]["_id"]
            parentId = data_array[0]["parentId"]
            collect_info_map["_id"] = _id
            collect_info_map["parentId"] = parentId
            print("查询获取的集合信息:", collect_info_map)
            return collect_info_map
    else:
        return None


# 创建空集合目录  文件夹:folder   手动集合:virtual
def create_collection(parentId, collectionName, type):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    data = {
        "datasetId": datasetId,
        "parentId": parentId,
        "name": collectionName,
        "type": type,
        "metadata": {}
    }
    response = requests.post(collectionUrl, data=json.dumps(data), headers=headers)
    # 检查响应状态码并输出响应内容
    if response.status_code == 200:
        print('创建成功--' + type + collectionName)
        response_json = response.json()
        data = response_json.get('data', {})
        if data:
            return data


# 手动集合中插入记录
def insert_data(collectionId, q, a):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    data = {
        "collectionId": collectionId,
        "q": q,
        "a": a,
        "indexes": []
    }
    response = requests.post(insertUtl, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print('记录插入成功--' + q)
        return True
    else:
        return False


# 向集合中批量添加数据
# 参数传入记录集合
# 注意：每次最多推送 200 组数据
#       同一组数据最好在业务上属于相同范围,这样放入相同的集合好管理
# trainingMode = chunk/qa
def push_data(collectionId, trainingMode, records):
    records_map_list = []
    for record in records:
        qa_pair = {
            "q": record,
            "a": ""
        }
        records_map_list.append(qa_pair)

    headers = {
        'Authorization': 'Bearer ' + appKey,
        'Content-Type': 'application/json'
    }
    data_raw = {
        "collectionId": collectionId,
        "trainingMode": trainingMode,
        # "prompt": '',
        # "billId": "",
        "data": records_map_list
    }
    response = requests.post(pushUrl, data=json.dumps(data_raw), headers=headers)
    code = response.status_code
    if code == 200:
        print('批量记录插入成功--')
        # print('批量记录插入成功--' + ','.join(str(i) for i in records))
        return True
    else:
        print('批量记录插入失败--')
        return False


# 获取token
def fastgpt_login(username, password):
    headers = {'Content-Type': 'application/json'}
    data = {
        "username": username,
        "password": password
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


# 批量创建知识库
def batch_create_dataset(parentId, datasetNames):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + appKey
    }
    for datasetName in datasetNames:
        data = {
            'agentModel': 'moonshot-v1-128k',
            'avatar': '/icon/logo.svg',
            'name': '企业基础数据-' + datasetName,
            'intro': '',
            'parentId': parentId,
            'type': 'dataset',
            'vectorModel': 'm3e'
        }
        response = requests.post(datasetUrl, data=json.dumps(data), headers=headers)
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
    # insert_data("66729d7327c7172c8149bcb9","test","")

    # param = ["1","2","3"]
    # re = push_data("66681eb9a1d4f2f9ce06b285","chunk",param)

    flag = True

    while flag:
        # 示例使用
        host = '192.168.201.75'
        database = 'stg_model'
        port = 9030
        user = 'root'
        password = '123456'

        query = ('select id'
                 ',concat_ws(\':\',\'公司名称\',IFNULL(company_name,\'暂无相关信息\')) as company_name'
                 ',concat_ws(\':\',\'成立时间\',IFNULL(establishment_date,\'暂无相关信息\')) as establishment_date'
                 ',concat_ws(\':\',\'公司简称\',IFNULL(company_abbreviation,\'暂无相关信息\')) as company_abbreviation'
                 ',concat_ws(\':\',\'注册资本\',IFNULL(registered_capital,\'暂无相关信息\')) as registered_capital'
                 ',concat_ws(\':\',\'注册资本币种\',IFNULL(currency_type,\'暂无相关信息\')) as currency_type'
                 ',concat_ws(\':\',\'公司类型\',IFNULL(company_type,\'暂无相关信息\')) as company_type'
                 ',concat_ws(\':\',\'公司性质\',IFNULL(company_nature,\'暂无相关信息\')) as company_nature'
                 ',concat_ws(\':\',\'法人代表\',IFNULL(legal_representative,\'暂无相关信息\')) as legal_representative'
                 ',concat_ws(\':\',\'注册地址\',IFNULL(registered_address,\'暂无相关信息\')) as registered_address'
                 ',concat_ws(\':\',\'国民经济分类\',IFNULL(economic_classification,\'暂无相关信息\')) as economic_classification'
                 ',concat_ws(\':\',\'战略新兴产业分类\',IFNULL(strategic_emerging_industry_classification,\'暂无相关信息\')) as strategic_emerging_industry_classification'
                 ',concat_ws(\':\',\'火石产业分类\',IFNULL(huoshi_industry_classification,\'暂无相关信息\')) as huoshi_industry_classification'
                 ',concat_ws(\':\',\'公司简介\',IFNULL(company_introduction,\'暂无相关信息\')) as company_introduction'
                 ',concat_ws(\':\',\'资质认证\',IFNULL(qualification_certification,\'暂无相关信息\')) as qualification_certification'
                 ',concat_ws(\':\',\'经营状态\',IFNULL(operational_status,\'暂无相关信息\')) as operational_status'
                 ',concat_ws(\':\',\'资产总额\',IFNULL(total_assets,\'暂无相关信息\')) as total_assets'
                 ',concat_ws(\':\',\'所有者权益合计\',IFNULL(total_equity,\'暂无相关信息\')) as total_equity'
                 ',concat_ws(\':\',\'净利润\',IFNULL(net_profit,\'暂无相关信息\')) as net_profit'
                 ',concat_ws(\':\',\'主营业务收入\',IFNULL(main_business_income,\'暂无相关信息\')) as main_business_income'
                 ',concat_ws(\':\',\'负债总额\',IFNULL(total_liabilities,\'暂无相关信息\')) as total_liabilities'
                 ',concat_ws(\':\',\'纳税总额\',IFNULL(total_taxes,\'暂无相关信息\')) as total_taxes'
                 ',concat_ws(\':\',\'营业总收入\',IFNULL(total_operating_income,\'暂无相关信息\')) as total_operating_income'
                 ',concat_ws(\':\',\'利润总额\',IFNULL(total_profit,\'暂无相关信息\')) as total_profit'
                 ',concat_ws(\':\',\'融资信息\',IFNULL(financing_info,\'暂无相关信息\')) as financing_info'
                 ',concat_ws(\':\',\'上市信息\',IFNULL(listing_info,\'暂无相关信息\')) as listing_info'
                 ',concat_ws(\':\',\'并购信息\',IFNULL(merger_acquisition_info,\'暂无相关信息\')) as merger_acquisition_info'
                 ',concat_ws(\':\',\'办公地址\',IFNULL(office_address,\'暂无相关信息\')) as office_address'
                 ',concat_ws(\':\',\'所属国家\',IFNULL(country,\'暂无相关信息\')) as country'
                 ',concat_ws(\':\',\'所属省份\',IFNULL(province,\'暂无相关信息\')) as province'
                 ',concat_ws(\':\',\'所属城市\',IFNULL(city,\'暂无相关信息\')) as city'
                 ',concat_ws(\':\',\'所属区域\',IFNULL(area,\'暂无相关信息\')) as area '
                 'from stg_model.stg_company_basic_info '
                 'where handle_status = \'0\' '
                 'and province = \'%s\' and city = \'%s\' '
                 'and company_introduction is not null '
                 'and company_name is not null '
                 'limit 10000')
        #
        query_module = 'select province ,city from stg_model.stg_company_basic_info where province is not null and city is not null and  handle_status = \'0\' group by province ,city order by province ,city ;'

        collection_list_not_process = list(read_mysql_data_v1(host, database, user, password, port, query_module))

        if collection_list_not_process is not None:
            parm = []
            for i in collection_list_not_process:
                ii = (i[0], i[1])
                parm.append(ii)

            token = fastgpt_login(fast_username, fast_password)
            for sub_parm in parm:
                sub_flag = True
                while sub_flag:
                    final_query = query % sub_parm
                    records = read_mysql_data_v1(host, database, user, password, port, final_query)

                    tag = not records
                    if not tag:
                        mid_process(records, token, parentId, datasetId, host, port, user, password, database)
                    else:
                        sub_flag = False
        else:
            print("全部处理完成")
            flag = False

        # read_mysql_data(host, database, user, password, port, query)

    print("全部执行完成")
