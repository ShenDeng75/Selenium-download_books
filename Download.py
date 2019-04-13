#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
from Tools import Print_Color as pc
from Tools import File_Manage as fm
import random
import re

# 控制下载页面
def Downloads(driver):
    fn = []   # 需要重命名的文件列表
    for i in range(3):
        print("开始下载第 %d 页" % int(i+1))
        ans = Download(driver, i, fn)
        if ans:
            break
        time.sleep(3)   # 等待上一页最后一个文件的添加
    with open(r'D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/rename_file.txt', 'w', encoding='utf-8') as f:
        json.dump(fn, f)
    input("按任意键对文件重命名：")
    for f in fn:
        fm.renameFile("D:/Google/下载数据/最新下载", f)
# 下载
def Download(driver, page, fn):
    url = "http://cn.epubee.com/files.aspx?sortkey=&sort=&menukey=&menuvalue=&Page={0}".format(page)
    driver.get(url)
    time.sleep(2)   # 等待页面加载，使元素可见
    downloads = driver.find_elements_by_class_name("parent")   # 获取待下载的书列表
    with open(r"D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/IsDown_books.txt", 'r', encoding='utf-8') as f:   # 获取已下载的书列表
        IsDown_books = json.load(f)
    downloads.reverse()   # 由上到下下载，会出现遮挡，所以由下到上下载
    for download in downloads:
        try:
            title1 = str(download.find_elements_by_class_name("titleshow")[1].text)  # 获取待下载书名
            title2 = title1.encode('gbk', "ignore").decode('gbk')   # 去除GBK无法编码的字符
            title = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", " ", title2)   # 去除不可用于命名的字符
            ok = 1
            for b in IsDown_books:   # 如果已经下载
                if title in b:
                   pc.Print(title + "...........已经下载！", pc.yellow)
                   ok = 0
                   break
            if not ok:
                continue
        except:
            pc.Print("页面错误", pc.red)
            load(IsDown_books)
            return -1
        try:
            down = download.find_element_by_class_name("child_extension")
            driver.execute_script("arguments[0].click();", down)  # 点击下载
            pc.Print("-------下载了：" + title, pc.green)
            IsDown_books.append(title)   # 更新已下载书列表
            time.sleep(3)   # 等待文件添加到文件夹
            fn.append(title)   # 加入到重命名文件列表
            time.sleep(random.uniform(3, 7))   # 下载延时，防止被封
        except Exception as e:
            pc.Print(title + "*********下载失败！", pc.red)
            pc.Print("未知错误！" + str(e), pc.red)
            continue
    load(IsDown_books)
    return 0

def load(IsDown_books):
    with open(r"D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/IsDown_books.txt", 'w', encoding='utf-8') as f:
        json.dump(IsDown_books, f, ensure_ascii=False)