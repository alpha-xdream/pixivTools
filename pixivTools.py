# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:15:23 2017

@author: alphaXdream

1000users入り
Test url:https://www.pixiv.net/search.php?s_mode=s_tag_full&word=%E3%83%A6%E3%82%B0%E3%83%89%E3%83%A9%E3%82%B7%E3%83%AB(%E3%82%B0%E3%83%A9%E3%83%96%E3%83%AB)

"""

import requests
import re
import time
import random
import os
from bs4 import BeautifulSoup
user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
base_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
login_url = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
    # headers只要这两个就可以了,之前加了太多其他的反而爬不上
headers = {
    'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
    'User-Agent': random.choice(user_agent_list)
}

def login():
    pixiv_id = 'lin.xr@foxmail.com'
    f = open('info.txt')
    password = f.readline()
    print(password)
    f.close()
    post_key = []
    return_to = 'https://www.pixiv.net/'
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
    s.post(login_url, data=data, headers=headers,allow_redirects=False)
    
def getHTMLText(url):
    return s.get(url).text

def saveRankPic(url):
    count = -1# &p=2
    p = 1
    infos = []
    while count!=0:
        text = getHTMLText(url+'&p='+str(p))
        p = p+1
        soup = BeautifulSoup(text,"lxml")
        if count==-1:
            count = int(soup.find('span',{'class':'count-badge'}).get_text()[:-1])
        for item in soup.find_all('li',{'class':'image-item'}):
            count = count - 1
            img_link = website+item.a['href']
            title = item.find('h1',{'class':'title'}).get_text()
            author = item.find('a',{'class':'user ui-profile-popup'}).get_text()
            if item.find('a',{'class':'bookmark-count _ui-tooltip'}) is not None:
                star = int(item.find('a',{'class':'bookmark-count _ui-tooltip'}).get_text())
            else:
                star = 0
            infos.append((star,author,title,img_link)) #按照收藏数、作者、标题、图片链接的顺序存放
            
            '''
            print('图片链接：'+website+item.a['href'])
            print('标题：'+item.find('h1',{'class':'title'}).get_text())
            print('作者：'+item.find('a',{'class':'user ui-profile-popup'}).get_text())
            print('收藏数：'+item.find('a',{'class':'bookmark-count _ui-tooltip'}).get_text())
            t = item.find('img',{'class':'_thumbnail ui-scroll-view '})['data-src']
            t = re.sub(r'c/150x150/img-master','img-original',t)
            t = re.sub(r'_master1200','',t)
            print('正在下载：'+t)
            try:
                tmp = headers
                tmp['Referer'] = t
                pic= s.get(t,headers=tmp)
            except requests.exceptions.ConnectionError:
                print('当前图片无法下载')
                continue
            file = open('pic2/'+t.split(r'/')[-1],'wb')
            file.write(pic.content)
            file.close()
            time.sleep(5)'''
    infos.sort(reverse=True)
    file = open('rank.txt','w',encoding='utf-8')#收藏数、作者、标题、图片链接
    for item in infos:
        file.write('收藏数:'+str(item[0])+'\n')
        file.write('作者:'+item[1]+'\n')
        file.write('标题:'+item[2]+'\n')
        file.write('图片链接:'+item[3])
        file.write('\n'*3)
    file.close()

def downloadPicByAuthor(url):
    count = -1# &p=2
    p = 1
    infos = []
    while count!=0:
        text = getHTMLText(url+'&p='+str(p))
        p = p+1
        soup = BeautifulSoup(text,"lxml")
        #user
        author = soup.find('h1',{'class':'user'}).get_text()
        if count==-1:
            count = int(soup.find('span',{'class':'count-badge'}).get_text()[:-1])
        for item in soup.find_all('li',{'class':'image-item'}):
            count = count - 1
            img_link = website+item.a['href']
            t = item.find('img',{'class':'_thumbnail ui-scroll-view '})['data-src']
            t = re.sub(r'c/150x150/img-master','img-original',t)
            t = re.sub(r'_master1200','',t)
            try:
                tmp = headers
                tmp['Referer'] = img_link
                pic= s.get(t,headers=tmp)
            except requests.exceptions.ConnectionError:
                print('当前图片无法下载')
                continue
            if not os.path.exists(author):
                os.mkdir(author)
            file = open(author+'/'+t.split(r'/')[-1],'wb')
            file.write(pic.content)
            file.close()
            time.sleep(5)
s = requests.Session()
login()
website = 'https://www.pixiv.net'
url = "https://www.pixiv.net/search.php?s_mode=s_tag_full&word=%E3%83%A6%E3%82%B0%E3%83%89%E3%83%A9%E3%82%B7%E3%83%AB(%E3%82%B0%E3%83%A9%E3%83%96%E3%83%AB)"
saveRankPic(url)
author_url = 'https://www.pixiv.net/member_illust.php?id=1055457'
downloadPicByAuthor(author_url)