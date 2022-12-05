from typing import Optional
import re

import requests
import ddddocr
from retry import retry

__all__ = ['LoginBot']


class LoginBot(object):
    def __init__(self, email_or_telephone_number: str, password: str,
                 use_gpu: bool = False, device_id: int = 0):
        """
        模拟登录API类。
        使用__init__函数不会进行爬虫。
        
        :raise: 当格式不正确时引发ValueError
        :param email_or_telephone_number: 邮箱/手机号，手机号仅支持
        :param password: 登录密码
        :param use_gpu: 是否使用GPU识别验证码，默认为False
        :param device_id: 识别验证码的设备号，默认为0
        """
        self.username = email_or_telephone_number
        self.password = password
        self.verification()
        self.ocr = ddddocr.DdddOcr(use_gpu, device_id)
        
    def verification(self):
        """
        检验密码和邮箱/手机号的格式。
        
        :raise: 当格式不正确时引发ValueError
        :return: None
        """
        if not 6 <= len(self.password) <= 20:
            raise ValueError('incorrect password format, length must be between 6~20')
        # 仅支持移动、联通和电信的11位手机号
        mobile = re.compile('(134|135|136|137|138|139|150|151|152|157|158|159|182|183|184'
                            '|187|188|147|178|1705)[1-9]+')  # 中国移动
        union = re.compile('(130|131|132|155|156|185|186|145|176|1709)[1-9]+')  # 中国联通
        telecom = re.compile('(13|153|180|181|189|177|1700)[1-9]+')   # 中国电信
        if mobile.search(self.username) or union.search(self.username) or telecom.search(self.username):  # 是手机号
            return
        email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(email, self.username):
            return
        raise ValueError('not a valid phone number or a email address')
    
    def login(self, session: Optional[requests.Session] = None) -> requests.Session:
        """
        进行模拟登录。
        
        :param session: requests.Session类型，用于爬虫。如果为None则新建一个session
        :return: 完成登录后的session
        """
        if session is None:
            session = requests.session()
        self._login(session)
        return session
    
    @retry(tries=5)
    def _login(self, session: requests.Session) -> None:
        captcha_url = 'https://so.gushiwen.cn/RandCode.ashx'
        img = session.get(captcha_url)
        captcha = self.ocr.classification(img.content)
        post_url = 'https://so.gushiwen.cn/user/login.aspx'
        data = {
            'email': self.username,
            'pwd': self.password,
            'code': captcha,
            'denglu': '\u767b\u5f55',
        }
        session.post(post_url, data=data)
