
file_path = "/Users/jinmu/Downloads/20220227笔记"
fo = open(file_path,'r')

#获取文件属性
print(fo.name)

#读取内容
str = fo.read(200)
print(str)
position = fo.tell()
print("读取到的位置 = " , position)

#seek()重置position
fo.seek(0,0)
print("读取到的位置 = " , fo.tell())
line = fo.readline()
print("读取一行 = " + line)


import os

#重命名
#os.rename("/Users/jinmu/Downloads/企业服务  .xlsx","/Users/jinmu/Downloads/企业服务-1.xlsx")

#关闭
fo.close()




