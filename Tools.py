#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
   工具类
'''
import os
import re
import json

# 在控制台输出有颜色的字
class Print_Color():
    green = "green"
    yellow = "yellow"
    red = "red"

    # 在控制台输出有颜色的字
    @staticmethod
    def Print(str, color):
        colorMap = {"green": 32, "yellow": 33, "red": 31}
        cstr = "\033[{0}m{1}\033[0m".format(colorMap[color], str)
        print(cstr)

# 文件管理
class File_Manage():

    # 删除单个文件夹中重复文件。
    @staticmethod
    def overKill(path):
        files = os.listdir(path)
        for f in files:
            if re.findall(r'.*\(\d\)\.', f):
                os.remove(path+"/"+f)
                print("已删除重复书籍：", f)

    # 在一个文件夹中删除出现在另一个文件夹中的文件
    @staticmethod
    def overKills(p_path, c_path):
        p_files = os.listdir(p_path)
        c_files = os.listdir(c_path)
        for f in c_files:
            if p_files.count(f):
                os.remove(c_path + "/" +f)
                print("已删除文件夹 [%s] 中的文件 [%s] !" % (c_path.rsplit('\\', 1)[1], f))

    # 在一个文件夹中，为一个文件修改名字(针对自动下载电子书)。
    @staticmethod
    def renameFile(path, name):
        files = os.listdir(path)
        load_name = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", name).lower()   # 中文，字母，数字
        find_file = [x for x in files if load_name in x]
        if find_file:
            old_name = path+"/"+find_file[0]
            new_name = path+"/"+name+"."+str(find_file[0]).split('.')[-1]
            try:
               os.rename(old_name, new_name)
            except FileExistsError:
                os.remove(old_name)
                print("文件已存在，已删除此文件")
            print("修改成功")
        else:
            Print_Color.Print("没有找到文件"+name, Print_Color.red)

if __name__ == "__main__":
    with open(r"D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/rename_file.txt", 'r', encoding='utf-8') as f:
        rname = json.load(f)
    for f in rname:
       File_Manage.renameFile("D:/Google/下载数据/最新下载", f)
    pass