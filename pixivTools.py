# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:15:23 2017

@author: alphaXdream

Test url:https://www.pixiv.net/search.php?s_mode=s_tag_full&word=%E3%83%A6%E3%82%B0%E3%83%89%E3%83%A9%E3%82%B7%E3%83%AB(%E3%82%B0%E3%83%A9%E3%83%96%E3%83%AB)

"""

import requests
import re
from bs4 import BeautifulSoup

#s = requests.Session()
def login():
    base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
    login_url = 'https://accounts.pixiv.net/api/login?lang=zh'
    # headers只要这两个就可以了,之前加了太多其他的反而爬不上
    headers = {
        'Host': "accounts.pixiv.net", 
        'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Connection': 'keep-alive'
    }
    pixiv_id = 'lin.xr@foxmail.com'
    f = open('info.txt')
    password = f.readline()
    print(password)
    f.close()
    post_key = []
    return_to = 'http://www.pixiv.net/'
    post_key_html = s.get(base_url, headers=headers).text
    pattern = re.compile('<input type="hidden".*?value="(.*?)">', re.S)  
    result = re.search(pattern, post_key_html) 
    post_key = result.group(1)
    # 上面是去捕获postkey
    data = {
        'pixiv_id': pixiv_id,
        'password': password,
        'return_to': return_to,
        'post_key': post_key
    }
    s.post(login_url, data=data, headers=headers)
    
def getHTMLText(url):
    return s.get(url).text

#login()
website = 'https://www.pixiv.net'
url = "https://www.pixiv.net/search.php?s_mode=s_tag_full&word=%E3%83%A6%E3%82%B0%E3%83%89%E3%83%A9%E3%82%B7%E3%83%AB(%E3%82%B0%E3%83%A9%E3%83%96%E3%83%AB)"
text = getHTMLText(url)
soup = BeautifulSoup(text,"lxml")
for item in soup.find_all('li',{'class':'image-item'}):
    print('图片链接：'+item.a['href'])
    print('标题：'+item.find('h1',{'class':'title'}).get_text())
    print('作者：'+item.find('a',{'class':'user ui-profile-popup'}).get_text())
    print('收藏数：'+item.find('a',{'class':'bookmark-count _ui-tooltip'}).get_text())
    print('正在下载：'+item.find('img',{'class':'_thumbnail ui-scroll-view '})['data-src'])


