#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
   测试类
'''
import json
import os
from Tools import File_Manage as fm
import re

def IsSave():  # 已经保存的
    save = []
    with open(r"./Content/IsSave_books.txt", 'r', encoding='utf-8') as f:
        save = json.load(f)
    print("已经保存的："+str(len(save)))
    return save

def IsDown():
    down = []   # 已经下载的
    with open(r"./Content/IsDown_books.txt", 'r', encoding='utf-8') as f:
        down = json.load(f)
    print("已经下载的："+str(len(down)))
    # print(down)
    return down

def IsLoad():   # 实际下载的
    path = r"D:\Google\下载数据\下载的电子书"
    new_path = r"D:\Google\下载数据\最新下载"
    local = os.listdir(path) # [re.findall(r'(.*?)\d{5,8}', x)[0].replace('_', '').replace(' ', '') for x in os.listdir(path)]
    new_local = os.listdir(new_path) # [re.findall(r'(.*?)\d{5,8}', x)[0].replace('_', '').replace(' ', '') for x in os.listdir(new_path)]
    local += new_local
    print("实际下载的："+str(len(local)))
    # print(local)
    for f in local:
        if re.findall(r'.*\(\d\)\.', f):
            print("重复书籍：", f)
    return local

def Sync(local):   # 同步。注：同步时，会把IsDown_books中的':'改成'_'导致下载重复的书。
    with open(r"./Content/IsSave_books.txt", 'w', encoding='utf-8') as f:
        json.dump(local, f)
    with open(r"./Content/IsDown_books.txt", 'w', encoding='utf-8') as f:
        json.dump(local, f)
    print("已同步!")

def Nolocal(down, local):    # 添加了，但未下载
    ans = list(set(down) - set(local))
    print("添加了但未下载："+str(len(ans)))
    print(ans)
    return ans

def test():
    save = IsSave()
    down = IsDown()
    local = IsLoad()

if __name__ == "__main__":
    test()
    sum_path = r"D:\Google\下载数据\下载的电子书"
    new_path = r"D:\Google\下载数据\最新下载"
    Sync(IsLoad())  # 把IsSave和IsDown与local同步
    fm.overKill(new_path)  # 删除单个文件夹重复的书
    # fm.overKills(sum_path, new_path)   # 删除不同文件夹中的重复文件
    # Nolocal(down, local)   # 添加了但未下载
