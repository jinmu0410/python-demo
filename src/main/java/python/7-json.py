import json

## 字典类型
data = {
    'id': 1,
    'name': '张三',
    'age': 20
}

json_data = json.dumps(data)

print(repr(data))
print(json_data)

