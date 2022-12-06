这是一个关于爬取古诗文的Python3 API。  
此库请求了古诗文网(https://www.gushiwen.cn/)，并下载诗词信息。  
建议到古诗文网上创建账号，并使用此库提供的模拟登录API，可以避免请求频繁。  

# 创建第一个pygushi程序

## 安装
首先，我们需要在python中安装`pygushi`:  
使用`pip`:
```shell
pip install pygushi
```
使用`git`:
```shell
git clone https://github.com/stripepython/pygushi
cd pygushi
python setup.py install
```

## 准备 
进入古诗文网“我的”页面，并创建一个账号：    
创建账号的页面为[https://so.gushiwen.cn/user/register.aspx](https://so.gushiwen.cn/user/register.aspx)。

## 开始编写
现在，我们将获取一些“绝句”有关的诗歌。  
首先，导入`pygushi`:
```python
import pygushi
```

接下来，使用模拟登录API进行登录(其实这一步没有也可以，但建议添加，以免不必要的BUG)：
```python
import pygushi
login_bot = pygushi.LoginBot('刚才注册的手机号码或电子邮箱', '你的密码')
session = login_bot.login()
```

然后，调用搜索API，获取与“绝句”有关的诗词ID:
```python
import pygushi
login_bot = pygushi.LoginBot('刚才注册的手机号码或电子邮箱', '你的密码')
session = login_bot.login()
poetries = pygushi.PoetryBot.search('绝句', session)
```

接下来，依次遍历，将它们输出在控制台，这就是这一demo的完整代码：
```python
import pygushi
login_bot = pygushi.LoginBot('刚才注册的手机号码或电子邮箱', '你的密码')
session = login_bot.login()
poetries = pygushi.PoetryBot.search('绝句', session)
for pbot in poetries:
    text = pbot.get().prettify()
    print(text)
```
```
           绝句          
           杜甫          
两个黄鹂鸣翠柳，一行白鹭上青天。
窗含西岭千秋雪，门泊东吴万里船。
          江南春          
           杜牧          
千里莺啼绿映红，水村山郭酒旗风。
南朝四百八十寺，多少楼台烟雨中。
        夏日绝句       
        李清照        
生当作人杰，死亦为鬼雄。
至今思项羽，不肯过江东。
        绝句二首       
         杜甫        
迟日江山丽，春风花草香。
泥融飞燕子，沙暖睡鸳鸯。
江碧鸟逾白，山青花欲燃。
今春看又过，何日是归年。
           绝句          
           志南          
古木阴中系短篷，杖藜扶我过桥东。
沾衣欲湿杏花雨，吹面不寒杨柳风。
(其余省略)
```

# 详细文档
接下来的内容是更详细的介绍。  
pygushi使用了面向对象的结构。

## 前言
pygushi的整体代码(不含注释)仅仅只有200多行。  
因此，它调用了许多API。  
其中的验证码识别使用了ONNX模型，这种模型在Mac上不太适用。

## pygushi.version
这是一个`namedtuple`，其具有major, minor, micro三个属性。  
如下是一个简单实例：
```python
from pygushi import version
assert version >= (1, 2, 0)
```

## pygushi.Author
这是一个作者数据类，它的初始化方法如下：
```python
Author(
    name: str, 
    brief_introduction: Optional[str] = None, 
    image: Optional[PIL.Image.Image] = None
)
```
- name：作者姓名
- brief_introduction: 简介
- image：作者头像

## pygushi.Poetry
这是一个诗词数据类，它的初始化方法如下：

```python
Poetry(
    title: str,
    content: str,
    translation: Optional[str] = None,
    notes: Optional[str] = None,
    author: Optional[Union[Author, str]] = None
)
```

- title：诗词标题
- content：诗词内容
- translation：译文
- notes：注释
- author：作者

### pygushi.Poetry.sentences
```python
Poetry.sentences(
    self,
    split_chars: Sequence[str] = _DEFAULT_SPLITS,
    filter_notes: bool = False
) -> List[str]
```
获取此诗词的句子列表。
- `split_chars`: 一个序列，遇到哪些字符算作一句，默认为中文的句号、问号、叹号和分号。
- `filter_notes`: 当此参数为True时，将忽略`()`内的注释内容。

### pygushi.Poetry.prettify
```python
Poetry.prettify(
    self, 
    split_chars: Sequence[str] = _DEFAULT_SPLITS,
    filter_nodes: bool = True, 
    fill_length: int = 7
) -> str
```
获取这一诗词的可视化形式。你可以将它输出在控制台。
- `split_chars`: 一个序列，遇到哪些字符算作一句，默认为中文的句号、问号、叹号和分号。
- `filter_notes`: 当此参数为True时，将忽略`()`内的注释内容。
- `fill_length`: 自适应的填充间距。在不同的格式和字体下该参数需要自行调整。

```python
from pygushi import PoetryBot
bot = PoetryBot('c35a60c1a8e2')
print(bot.get().prettify())
```
输出：
```
               静夜思
                李白
        床前明月光，疑是地上霜。
        举头望明月，低头思故乡。
```        

### pygushi.LoginBot
模拟登录API类。初始化方法：
```python
LoginBot(
    email_or_telephone_number: str, 
    password: str,
    use_gpu: bool = False, 
    device_id: int = 0
)
```
- `email_or_telephone_number`: 在古诗文网上注册的邮箱/手机号，手机号仅支持移动、联通和电信的11位手机号
- `password`: 在古诗文网上注册的密码
- `use_gpu`: 是否使用GPU识别验证码
- `device_id`: 识别验证码的设备号，默认为0

#### pygushi.LoginBot.login
```python
LoginBot.login(
    session: Optional[requests.Session] = None
) -> requests.Session
```
进行模拟登录，返回登录状态的`session`
- `session`: requests.Session类型，用于爬虫。如果为None则新建一个session

### pygushi.AuthorBot
作者信息API类。
```python
AuthorBot(author_id: str)
```
- `author_id`: 作者ID号。  
*例如: 在李白的网页https://so.gushiwen.cn/authorv_b90660e3e492.aspx中，`b90660e3e492`就是作者ID号*
> Note: 一般来说，本API不会让您使用ID号。

#### pygushi.AuthorBot.get
获取作者信息。
```python
get(
    self, 
    session: Optional[requests.Session] = None, 
    parser: str = 'html.parser'
) -> Author:
```
- `session`: requests.Session类型，用于爬虫。如果为None则新建一个session
- `parser`: beautifulsoup4解析器

**`parser`说明：**

| 值             | 意义              | 优点  | 缺点     |
|---------------|-----------------|-----|--------|
| `html.parser` | 使用`python`标准解析器 | 速度适中，不需要其他依赖 | 容错能力稍差 |
| `lxml` | 使用`lxml`解析器 | 速度快 | 需要安装`C`库和`lxml`扩展 |
| `html5lib` | 使用`html5lib`解析器 | 容错能力很强 | 需要`html5lib`扩展，速度慢 |

#### pygushi.AuthorBot.search
一个静态构造方法，通过古诗文网的API搜索作者信息并返回。如果没有这一作者，其将返回None.
```python
@staticmethod
search(
    name: str, 
    session: Optional[requests.Session] = None, 
    parser: str = 'html.parser'
) -> Optional[AuthorBot]
```
- `name`: 作者姓名
- `session`: requests.Session类型，用于爬虫。如果为None则新建一个session
- `parser`: beautifulsoup4解析器

### pygushi.PoetryBot
诗词信息API类。
```python
PoetryBot(poetry_id: str)
```
- `poetry_id`: 诗词ID

#### pygushi.PoetryBot.get
```python
PoetryBot.get(
    self, 
    session: Optional[requests.Session] = None, 
    parser: str = 'html.parser',
    get_author: bool = True
) -> Poetry
```
获取诗词信息，进行实际爬虫请求。

- `session`: requests.Session类型，用于爬虫。如果为None则新建一个session
- `parser`: beautifulsoup4解析器，详细说明见文档
- `get_author`: 是否自动爬取作者信息。当此项为True时，返回值的author属性是一个Author类的实例。否则，author属性是一个字符串，表示作者ID

#### pygushi.PoetryBot.search
一个静态构造方法，通过古诗文网的API搜索诗词信息并返回。返回一个由PoetryBot类实例构成的可变列表。
```python
@staticmethod
PoetryBot.search(
    name: str, 
    session: Optional[requests.Session] = None,
    parser: str = 'html.parser'
) -> List[PoetryBot]
```
- `name`: 诗词名称
- `session`: requests.Session类型，用于爬虫。如果为None则新建一个session
- `parser`: beautifulsoup4解析器，详细说明见文档

返回PoetryBot类实例(与诗词名称相关的诗词ID)列表。
