from typing import Optional, List
import re

import requests
from bs4 import BeautifulSoup

from .datas import Poetry
from .author import AuthorBot

__all__ = ['PoetryBot']


class PoetryBot(object):
    def __init__(self, poetry_id: str):
        """
        诗词信息API类。
        使用__init__函数不会进行爬虫。
        
        :param poetry_id: 诗词ID
        """
        self.id = poetry_id
        self.url = f'https://so.gushiwen.cn/shiwenv_{poetry_id}.aspx'
        
    def get(self, session: Optional[requests.Session] = None, parser: str = 'html.parser',
            get_author: bool = True) -> Poetry:
        """
        获取诗词信息，进行实际爬虫请求。
        
        :param session: requests.Session类型，用于爬虫。如果为None则新建一个session
        :param parser: beautifulsoup4解析器，详细说明见文档
        :param get_author: 是否自动爬取作者信息。当此项为True时，返回值的author属性是一个Author类的实例。
        否则，author属性是一个字符串，表示作者ID。
        :return: 诗词信息，Poetry类的实例
        """
        if session is None:
            session = requests.session()
        response = session.get(self.url)
        response.encoding = 'utf-8'
        if response.url == 'https://www.gushiwen.cn/':
            raise ValueError('no information about this poetry')
        soup = BeautifulSoup(response.text, parser)
        
        div = soup.find('div', class_='main3')
        if not div:
            raise ValueError('no information about this poetry')
        div = div.find('div', class_='left')
        if not div:
            raise ValueError('no information about this poetry')
        
        # 获取标题和内容
        cont = div.find('div', id='sonsyuanwen').find('div', class_='cont')
        title = cont.find('h1').text.strip()
        div_poem = div.find('div', class_='contson')
        content = div_poem.text.strip('\r').strip('\n').strip()
            
        # 获取译文和注释
        trans = div.find('div', class_='contyishang')
        tn = trans.find_all('p')
        translation = notes = None
        if len(tn) >= 1:
            translation_content = tn[0]
            translation = translation_content.text.replace('\u8bd1\u6587', '')
            idx = translation.find('\r')
            if idx != -1:
                translation = translation[:idx]
        if len(tn) >= 2:
            notes_content = tn[1]
            notes = notes_content.text.replace('\u6ce8\u91ca', '')
            
        author_div = div.find('div', class_='sonspic')
        cont = author_div.find('div', class_='cont')
        img = author_div.find('div', class_='divimg')
        a = cont.find_all('a')[bool(img)]  # 如果有图片，要找的a标签在第二个
        res_id = re.search('/authorv_(.*).aspx', a['href'])
        if not res_id:
            return None
        author = res_id.groups()[0]  # 作者id号
        if get_author:
            bot = AuthorBot(author)
            author = bot.get(session, parser)
        
        return Poetry(title, content, translation, notes, author)
    
    @staticmethod
    def search(name: str, session: Optional[requests.Session] = None,
               parser: str = 'html.parser') -> List['PoetryBot']:
        """
        一个静态构造方法，通过古诗文网的API搜索诗词信息并返回。
        返回一个由PoetryBot类实例构成的可变列表。
        
        :param name: 诗词名称
        :param session: requests.Session类型，用于爬虫。如果为None则新建一个session
        :param parser: beautifulsoup4解析器，详细说明见文档
        :return: PoetryBot类实例(与诗词名称相关的诗词ID)列表
        """
        if not name:
            raise ValueError('name is empty')
        if session is None:
            session = requests.session()
        res = []
        
        def search_one_page(page: int) -> List['PoetryBot']:
            """爬取一页信息"""
            url = f'https://so.gushiwen.cn/search.aspx?type=title&page={page}&value={name}&valuej={name[0]}'
            response = session.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, parser)
            div = soup.find('div', class_='main3').find('div', class_='left')
            if not div:
                return
            
            for sons in div.find_all('div', class_='sons'):
                if not sons:
                    continue
                cont = sons.find_next('div', class_='cont')
                p = cont.find('p')
                href = p.find('a')['href']
                res_id = re.search('/shiwenv_(.*).aspx', href)
                if not res_id:
                    continue
                res.append(PoetryBot(res_id.groups()[0]))
        
        # 古诗文网只有1、2页
        search_one_page(1)
        search_one_page(2)
        return res
