#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 用Cookies登录
import json
from selenium.webdriver.common.keys import Keys

# 登录
def Login(driver, url):
    driver.minimize_window()
    driver.delete_all_cookies()
    driver.get(url)   # 必须先访问该网站
    driver.delete_all_cookies()
    with open(r"D:/1文档/编程代码/PyCharm(Python)，代码/自动化代码/自动下载电子书/Content/cookies.txt", 'r') as f:   # 读取Cookies
        cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.set_page_load_timeout(5)  # 限制网页加载时间
    try:
        driver.get(url)
    except:
        Keys.ESCAPE    # 5秒后取消加载
    driver.set_page_load_timeout(16)