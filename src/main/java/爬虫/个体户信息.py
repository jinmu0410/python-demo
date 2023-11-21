import requests
import json
import pandas as pd
import time
import os
import urllib
from sqlalchemy import create_engine

#a1 对应地区编码(这个从平台中获取)
#a2 companyType 个体户对应5
#a3 pageIndex 1
#a4 pageSize 1000
def query(a1,a2,a3,a4,path):
    headers = {
        'Cookie':'UM_distinctid=18be54b16891124-030f6b11141f9d-16525634-1fa400-18be54b168a1a58; Hm_lvt_6b63cf9e50e2bd684eba62e24995ba09=1700358985; Hm_lvt_78d5885b19eecf93e59673b4b37c8530=1700358985; cna=2a89576bbc8f4def90f4c035046ccf36; tenantId=TPN1726055943878574082; sysAccountId=202311190100010003UEVR0000000082; acw_tc=781bad2917005330777712965e3f251e9f83ac6806671e33fd8dd2143f6a99; X-REALM-ORG=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdHgiOiJKU0VtNytteXZhcktSTVZTWnBMRzJ4RS9hVXc1VXlWVkVWYjgwbWc0U2RuSUFGcVFBKzk2NmVpR2NyemoydmhMaTNlTm1vbEJaeXJFSk53UEVxdktuWjRLTS9KcHZKL3dLTEpaWjFDS0FneE5qWVF6dGVRUXJRZ1ZYNmdmZ1YyNWJteDJITFd5ejJNSXBvUDY4RXkxQzc0K0d1WHlKVjlGdlJhdkV6SEJRa1U1VTg0V1FUTDRKMEJPbXBDNjVzVDNXSFlRZGVpMDlvYTZiWEU1UEpMMzE4RURMWkJ3aVlnUXBtUkRYa0kybEcwUVdyOWNNV1d4SDR1SjZ6UXA0T2FSQ2VUcjc0MzJFNmVOZTYrTVZZelBVd1V2WUFaS1g2OEZ3QTh5dFFCSk40N0NWY00xc2k0aVJ4cC9zSkkwUG5RemdIQnpPVUdGaDArMjdxeVp3K2JqWHNYN3Vmamp6T3R5N09IcE5raTdQUkRyQ0ZMRU9rRzIzMDBVRnpCeVZWbkxySW4yOFprTFIzTFJnTWE4RTV0bSs5MHRrYTdVOWV3czFnSXhhckJnYXIwPSIsImlzcyI6IlFKRCIsImVuYyI6dHJ1ZSwiZXhwIjoxNzAxMTM3ODc3LCJpYXQiOjE3MDA1MzMwNzcsImp0aSI6ImM3NDgwYWE3LWZjMzQtNDgxYS1hNGE2LWVjZjUxY2RhMTAwYyJ9.LjHhQFkjBjSLnEa8fENbkpQ0psJk9KH0C_g0NOnqyzA; Hm_lpvt_78d5885b19eecf93e59673b4b37c8530=1700533124; Hm_lpvt_6b63cf9e50e2bd684eba62e24995ba09=1700533124',
        'Origin':'https://www.sscha.com',
        'Referer':'https://www.sscha.com/',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua':'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'Accept':'application/json, text/plain, */*',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Type':'application/json;charset=UTF-8',
        'Host':'api.sscha.com'
    }

    str = '{"countryCodeList":[args1],"status":[1],"companyType":[args2],"searchType":21,"pageIndex":args3,"pageSize":args4}'
    data = str.replace('args1', a1, 1).replace('args2', a2, 1).replace('args3', a3,1).replace('args4', a4, 1)
    response = requests.post("https://api.sscha.com/center/company/pageCompany", headers = headers,data = data)


    print(response.text)
    if(response.status_code == 200):
        res = json.loads(response.text)['data']

        if res is None:
            print(response.text)
            return
        else:
            print("准备写入文件中")
            #saveExcel(res, path,a1)
            save_to_mysql(res)



def save_to_mysql(data):
    # 创建一个连接到 MySQL 数据库的引擎
    # 格式为：'mysql+mysqlconnector://username:password@hostname:port/database_name'
    encoded_password = urllib.parse.quote('R#m9@L7s$yFhN23')

    connection_string = f'mysql+mysqlconnector://aifish:{encoded_password}@47.97.231.182:3306/spider_man'
    engine = create_engine(connection_string)

    # 假设 df 是你的 Pandas DataFrame
    df = pd.DataFrame(data)
    df = df.astype(str)
    # 显式地打开连接
    connection = engine.connect()
    try:
        # 将 DataFrame 写入 MySQL 数据库中的表格
        table_name = 'company_data'  # 设定表格名称
        df.to_sql(table_name, con=connection, if_exists='append', index=False)

        # 数据写入完成后，手动关闭连接
        connection.close()
    except Exception as e:
        # 发生异常时关闭连接并处理异常
        connection.close()
        print("发生错误:", e)

def saveExcel(data, file_name, sheet_name):
    df = pd.DataFrame(data)
    if os.path.isfile(file_name):
        existing_data = pd.read_excel(file_name, sheet_name=None)
        if sheet_name in existing_data:
            start_row = existing_data[sheet_name].shape[0] + 1
            with pd.ExcelWriter(file_name, mode='a', engine='openpyxl',if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False, sheet_name=sheet_name, startrow=start_row)
        else:
            with pd.ExcelWriter(file_name, mode='a', engine='openpyxl',if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False, sheet_name=sheet_name)
    else:
        df.to_excel(file_name, sheet_name=sheet_name, index=False)
    print("保存成功" + file_name + " ----sheet---" + sheet_name)

if __name__ == '__main__':
    #330108 杭州-滨江
    #330102 杭州-上城
    #330105 杭州-拱墅
    #330106 杭州-西湖
    #330109 杭州-萧山
    #330110 杭州-余杭
    #330111 杭州-富阳
    #330112 杭州-临安
    #330113 杭州-临平
    #330114 杭州-钱塘
    #330122 杭州-桐庐
    #330127 杭州-淳安
    #330182 杭州-建德

   hangzhou_data_list = [
        "330102",
        "330105",
        "330106",
        "330108",
        "330109",
        "330110",
        "330111",
        "330112",
        "330113",
        "330114",
        "330122",
        "330127",
        "330182"
    ]

   ningbo_data_list = [
       "330203",
       "330205",
       "330206",
       "330211",
       "330212",
       "330213",
       "330225",
       "330226",
       "330281"
   ]
   wenzhou_data_list = [
       "330302",
       "330303",
       "330304",
       "330305",
       "330324",
       "330326",
       "330327",
       "330328",
       "330329",
       "330381",
       "330382",
       "330383"
   ]
   jiaxing_data_list = [
      "330402",
      "330411",
      "330421",
      "330424",
      "330481",
      "330482",
      "330483"
   ]
   huzhou_data_list = [
       "330502",
       "330503",
       "330521",
       "330522",
       "330523"
   ]

   shaoxing_data_list = [
       "330600",
       "330603",
       "330604",
       "330624",
       "330681",
       "330683"
   ]
   jinhua_data_list = [
       "330700",
       "330703",
       "330723",
       "330726",
       "330727",
       "330781",
       "330782",
       "330783",
       "330784"
   ]
   quzhou_data_list = [
       "330802",
       "330803",
       "330822",
       "330824",
       "330825",
       "330881"
   ]
   zhousan_data_list = [
       "330900",
       "330903",
       "330921",
       "330922"
   ]

   taizhou_data_list = [
       "331000",
       "331003",
       "331004",
       "331022",
       "331023",
       "331024",
       "331081",
       "331082",
       "331083"
   ]

   lishui_data_list = [
       "331100",
       "331121",
       "331122",
       "331123",
       "331124",
       "331125",
       "331126",
       "331127",
       "331181"
   ]

   path = "/Users/jinmu/Downloads/self/python-demo/src/main/java/爬虫/data/个体户/浙江/丽水.xlsx"


   test = [
       "820000",
       "710000"
   ]
   for x in test:
       for i in range(1,6):
           query(x,'5',str(i),'1000',path)
           time.sleep(2)
       time.sleep(1)

print("写入完成")

