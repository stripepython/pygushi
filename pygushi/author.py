import re
from typing import Optional
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL.Image import open

from .datas import Author

__all__ = ['AuthorBot']


class AuthorBot(object):
    def __init__(self, author_id: str):
        """
        作者信息API类。
        使用__init__函数不会进行爬虫。
        
        :param author_id: 作者ID号
        """
        self.id = author_id
        self.url = f'https://so.gushiwen.cn/authorv_{author_id}.aspx'
        
    def get(self, session: Optional[requests.Session] = None, parser: str = 'html.parser') -> Author:
        """
        获取作者信息，进行实际爬虫请求。
        
        :param session: requests.Session类型，用于爬虫。如果为None则新建一个session
        :param parser: beautifulsoup4解析器，详细说明见文档
        :raise: 当没有作者信息时引发ValueError
        :return: 作者信息，一个Author类的实例
        """
        if session is None:
            session = requests.session()
        response = session.get(self.url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, parser)
        # <div class="main3"><div class="left">...</div></div>
        div = soup.find('div', class_='main3').find('div', class_='left')
        if not div:
            raise ValueError('no information about this author')
        content = div.find('div', id='sonsyuanwen').find('div', class_='cont')  # 作者信息所在div
        
        # 试图获取图像
        img_div = content.find('div', class_='divimg')
        image = None
        if img_div:
            img_url = img_div.find('img')['src']
            response = session.get(img_url)
            io = BytesIO(response.content)
            image = open(io)
        
        name = content.find('h1').text.strip()  # 作者姓名
        brief = content.find('p').text.strip()  # 简介
        n = brief.find('\u25ba')
        if n != -1:
            brief = brief[:n]
        return Author(name, brief, image)
    
    @staticmethod
    def search(name: str, session: Optional[requests.Session] = None, parser: str = 'html.parser') -> Optional['AuthorBot']:
        """
        一个静态构造方法，通过古诗文网的API搜索作者信息并返回。
        如果没有这一作者，其将返回None.
        
        :param name: 作者姓名
        :param session: requests.Session类型，用于爬虫。如果为None则新建一个session
        :param parser: beautifulsoup4解析器，详细说明见文档
        :raise: 当姓名为空时引发ValueError
        :return: None或一个AuthorBot类的实例
        """
        if not name:
            raise ValueError('name is empty')
        if session is None:
            session = requests.session()
        url = f'https://so.gushiwen.cn/search.aspx?value={name}&valuej={name[0]}'
        response = session.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, parser)
        div = soup.find('div', class_='main3').find('div', class_='left')
        author = div.find('div', class_='sonspic')
        if not author:
            return None
        cont = author.find('div', class_='cont')
        img = author.find('div', class_='divimg')
        a = cont.find_all('a')[bool(img)]  # 如果有图片，要找的a标签在第二个
        res_id = re.search('/authorv_(.*).aspx', a['href'])
        if not res_id:
            return None
        return AuthorBot(res_id.groups()[0])
