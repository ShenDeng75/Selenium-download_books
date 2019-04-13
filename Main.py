#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
用Cookie登录cn.epubee.com网站并通过关键字搜索书籍，保存，下载。
工具：python3.6；selenium；chromedriver。
'''
from selenium import webdriver
from Login import Login
from Save2Cloud_ID import Save2Cloud_ID
from Download import Downloads
from Test import test, IsLoad, Sync

def get_driver():
    option = webdriver.ChromeOptions()   # 获取参数对象。
    # prefs = {"profile.managed_default_content_settings.images": 2,   # 不加载图片
    #          "profile.default_content_settings.popups": 0,    # 禁止弹窗
    #          "download.default_directory": 'D:\Google\下载数据\最新下载'}    # 设置文件下载路径
    # option.add_experimental_option("prefs", prefs)
    option.add_argument(r'--user-data-dir=D:\Google\自动化测试配置文件')   # 使用自己的配置文件，如果没有则会创建文件。
    driver = webdriver.Chrome(chrome_options=option)                    # 之后在chromedriver上的所有修改配置都会保存 New!!!
    return driver                                                        # 还会保存cookis
                                                                         # 但在打包时出现不能读取缓存的错误
def IsSync():
    arg = input("是否同步？[Y/N]：")
    if arg.lower() == 'y':
        local = IsLoad()
        Sync(local)
if __name__ == "__main__":
    url = "http://cn.epubee.com"
    driver = get_driver()
    # Login(driver, url)   # 配置文件中已经保留了Cookie，无需登录。
    Save2Cloud_ID(driver, url, 50)
    Downloads(driver)
    print("下载完毕")
    test()
    IsSync()