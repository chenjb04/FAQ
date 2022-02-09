# Python

## 递归处理list 成为树形json

```python
import json

list_data = [
    {'id': 1, 'name': '体育0', 'pid': 0},  # pid为0表示顶级
    {'id': 2, 'name': '体育1', 'pid': 1},  # pid的值等于id，则表示是那个元素的子级
    {'id': 3, 'name': '体育2', 'pid': 1},
    {'id': 4, 'name': '体育3', 'pid': 2},
    {'id': 5, 'name': '体育4', 'pid': 2},
    {'id': 6, 'name': '体育5', 'pid': 5},
    {'id': 7, 'name': '体育6', 'pid': 5},
    {'id': 8, 'name': '体育7', 'pid': 5},
    {'id': 8, 'name': '体育7', 'pid': 11},
]


def get_list(pid):
    data = []

    for x in list_data:
        if x['pid'] == pid:
            next_pid = x['id']
            x['children'] = get_list(next_pid)
            data.append({'name': x['name'], 'id': x['id'], 'children': x['children']})

    return data


print(get_list(0))
```

结果

```json
[
    {
        "name": "体育0", 
        "id": 1, 
        "children": [
            {
                "name": "体育1", 
                "id": 2, 
                "children": [
                    {
                        "name": "体育3", 
                        "id": 4, 
                        "children": [ ]
                    }, 
                    {
                        "name": "体育4", 
                        "id": 5, 
                        "children": [
                            {
                                "name": "体育5", 
                                "id": 6, 
                                "children": [ ]
                            }, 
                            {
                                "name": "体育6", 
                                "id": 7, 
                                "children": [ ]
                            }, 
                            {
                                "name": "体育7", 
                                "id": 8, 
                                "children": [ ]
                            }
                        ]
                    }
                ]
            }, 
            {
                "name": "体育2", 
                "id": 3, 
                "children": [ ]
            }
        ]
    }
]
```

## 列表字典去重

```python
# 第一种方法 reduce
from functools import reduce

list_data = [{'name': 'a'}, {'name': 'a'}, {'name': 'b'}]
list_data = list(reduce(lambda x, y: x if y in x else x + [y], [[], ] + list_data))

# 第二种方法
list_data = [dict(t) for t in set([tuple(d.items()) for d in list_data])]
# [{'name': 'a'}, {'name': 'b'}]
```

## 找出list中重复元素

```python
from collections import Counter
l = ['aa', 'aa', 'bb']
repeat_l = [k for k, v in dict(Counter(l)).items() if v > 1]
# ['aa']
```

## 求两个list的交集/并集/差集

```python
l1 = [1, 2, 3, 4, 5]
l2 = [1, 3, 5, 7, 8]

# 交集
print(list(set(l1).intersection(set(l2))))
# [1, 3, 5]

# 并集
# 方法1
print(list(set(l1).union(set(l2))))
# 方法2
print(list(set(l1) | set(l2)))
# [1, 2, 3, 4, 5, 7, 8]    

# 差集 
#  方法1 l1中有的 但是l2中没有的元素
print(list(set(l1) - set(l2)))
# 方法2
print(list(set(l1).difference(set(l2))))
# [2, 4]
```

##  获取指定长度随机字符串

```python
import secrets
import string


def gen_rand_str(length):
    """
    生成随机字符串
    :param length: 生成字符串的长度
    :return: 随机生成的字符串
    """
    # 包含特殊符号可以 chars = string.ascii_letters + string.digits + string.printable
    chars = string.ascii_letters + string.digits
    rand_str = ''.join(secrets.choice(chars) for _ in range(length))
    return rand_str


print(gen_rand_str(8))
```

## python zipfile 处理中文乱码问题

```python
import zipfile

zip_src = "要解压的zip文件路径"

with zipfile.ZipFile(zip_src) as fz:
    for file in fz.infolist():
        try:
            file.filename = file.filename.encode("cp437").decode("gbk")
        except:
            file.filename = file.filename.encode("utf-8").decode("utf-8")
        
        fz.extract(file, "要解压到的路径")
```

# sqlalchemy

## sqlalchemy开启事务

```python
session.begin(subtransactions=True)
# 最后需要commit 否则不生效
session.commit()


# 第二种方式
with db.session.begin_nested():
	pass
session.commit()
```

