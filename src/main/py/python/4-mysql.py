import pymysql

conn = pymysql.connect(host='192.168.110.40',user='root',password='Supcon_21',database='test',charset='utf8',port=3306)

cursor = conn.cursor()
query = "select * from test"
cursor.execute(query)
result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()
conn.close()
