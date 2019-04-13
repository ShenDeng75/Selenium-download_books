#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
from Tools import Print_Color as pc

# 保存
def Save2Cloud_ID(driver, url, maxCount):
    driver.get(url)
    # driver.minimize_window()
    time.sleep(2)
    words = get_word()
    s_key = driver.find_element_by_id("s_key")
    s_key.clear()   # 清空表单
    s_key.send_keys(words[0])   # 输入关键字
    driver.find_element_by_id("s_post").click()   # 点击搜索
    time.sleep(3)    # 等待加载
    ebookitems = driver.find_elements_by_class_name("ebookitem")   # 获取搜索的书列表
    with open(r"D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/IsSave_books.txt", 'r', encoding='utf-8') as f:   # 获得已存在的书列表
        exist_books = json.load(f)
    # maxCount = 40    # 添加的最大数量
    ow = 1   # 添加完一个关键字
    for book in ebookitems:
        title = str(book.text).split('[')[0].replace(' ', '').replace(':', '').replace('/', '')  # 获得书名
        if exist_books.count(title):   # 过滤已存在的书
            pc.Print(title+"..........已存在!", pc.yellow)
            continue
        save = book.find_element_by_link_text("保存到我的Cloud ID")
        driver.execute_script("arguments[0].click();", save)   # 使元素可见，再点击指定元素//New!!!
        time.sleep(3)
        if Out50(book):  # 如果已达50本上限
            ow -= 1
            break
        exist_books.append(title)   # 更新已存在的书
        maxCount -= 1
        pc.Print("---------保存了：" + title, pc.green)
        if not maxCount:    # 如果已达40本上限
            ow -= 1
            pc.Print("********已达50本上限(实际添加了50本)", pc.red)
            break
    with open(r"D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/IsSave_books.txt", 'w', encoding='utf-8') as f:   # 序列化已保存的书名
        json.dump(exist_books, f, ensure_ascii=False)
    if ow == 1:   # 表示此关键字已经添加完，并且还有添加的次数。
        pc.Print(words[0]+" 已添加完", pc.red)
        words.remove(words[0])
        set_word(words)
        Save2Cloud_ID(driver, url, maxCount)  # 递归把剩余的次数用完

def Out50(book):   # 判断是否达到50本上限
    try:
        book.find_element_by_link_text("成功")
        return False
    except:
        pc.Print("***********保存已达50本上限！！！", pc.red)
        return True

def get_word():   # 得到关键字列表
    with open(r"D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/wordKey.txt", 'r', encoding='utf-8') as f:
        words = json.load(f)
    return list(words)

def set_word(words):   # 序列化关键字列表
    with open(r"D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/wordKey.txt", 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False)