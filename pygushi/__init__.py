"""
这是一个关于爬取古诗文的Python3 API。

此库请求了古诗文网(https://www.gushiwen.cn/)，并下载诗词信息。

建议到古诗文网上创建账号，并使用此库提供的模拟登录API，可以避免请求频繁。

作者：stripe-python；
Python版本：3.7和3.8；
依赖项：ddddocr, requests, beautifulsoup4, pillow, retry, click；
系统要求：Windows和其他可以使用onnx模型的操作系统

导入方式：
>>> import pygushi
"""

from .login import LoginBot
from .author import AuthorBot
from .poetry import PoetryBot
from .version import version
from .datas import *

__version__ = '.'.join(str(i) for i in version)
__all__ = ['Author', 'AuthorBot', 'Poetry', 'PoetryBot', 'version']
