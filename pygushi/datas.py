from typing import Optional, Union, Sequence, List
from dataclasses import dataclass

from PIL.Image import Image

__all__ = ['Author', 'Poetry']

_DEFAULT_SPLITS = frozenset(
    {'\u3002', '\uff1f', '\uff01', '\uff1b'}
)  # 句号问号叹号分号


@dataclass
class Author(object):
    """
    作者数据类，使用@dataclass修饰。
    """
    
    name: str
    brief_introduction: Optional[str] = None
    image: Optional[Image] = None


@dataclass
class Poetry(object):
    """
    诗词数据类，使用@dataclass修饰。
    """
    
    title: str
    content: str
    translation: Optional[str] = None
    notes: Optional[str] = None
    author: Optional[Union[Author, str]] = None
    
    def sentences(self, split_chars: Sequence[str] = _DEFAULT_SPLITS,
                  filter_notes: bool = False) -> List[str]:
        """
        获取这一诗词的句子列表。
        
        :param split_chars: 一个序列，遇到哪些字符算作一句，默认为句号、问号、叹号和分号
        :param filter_notes: 是否忽略括号中的注释，默认为False
        :return: 句子列表
        """
        sentences = []
        current_item = ''
        in_filter = False
        for char in self.content:
            # 忽略()内的注释
            if char == '(' and filter_notes:
                in_filter = True
                continue
            if in_filter and char == ')':
                in_filter = False
                continue
                
            if not in_filter:
                current_item += char
            if char in split_chars:
                sentences.append(current_item.strip())
                current_item = ''
        return sentences
    
    def prettify(self, split_chars: Sequence[str] = _DEFAULT_SPLITS,
                 filter_nodes: bool = True, fill_length: int = 7) -> str:
        """
        获取这一诗词的可视化形式。
        
        >>> from pygushi import PoetryBot
        >>> bot = PoetryBot('c35a60c1a8e2')
        >>> bot.get().prettify()
               静夜思
                李白
        床前明月光，疑是地上霜。
        举头望明月，低头思故乡。
        
        当要以逗号分组时，建议将fill_length形参设为2：
        
        >>> bot.get().prettify(split_chars=['，', '。'], fill_length=2)
           静夜思
            李白
        床前明月光，
        疑是地上霜。
        举头望明月，
        低头思故乡。
        
        :param split_chars: 一个序列，遇到哪些字符算作一句，默认为句号、问号、叹号和分号
        :param filter_nodes: 是否忽略括号中的注释，默认为True
        :param fill_length: 修正映射长度值，使用默认字体时7最佳(默认值即7)，其他需要自行调整。
        :return: 这一诗词的可视化形式
        """
        # 获得可行的句子列表
        sentences = self.sentences(split_chars, filter_nodes)
        if not sentences:
            return ''
        # 以不同的字体显示时，缩进是不一样的
        # 这里采用了Pycharm中缩进量：7个单位
        mean = sum(map(len, sentences)) // len(sentences) + fill_length
        # 一个很有用的公式，通过计算平均句长来将标题映射到合适位置
        res = self.title.center(mean) + '\n'
        if isinstance(self.author, Author):
            res += self.author.name.center(mean) + '\n'
        res += '\n'.join(sentences)
        return res.strip('\n')
