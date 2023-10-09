## 查找自定路径下的指定文件
import os

path = '/Users/jinmu/Downloads/jars'
files = os.listdir(path)

for _ in files:
    if 'spline' in _:
        print('========'+_)