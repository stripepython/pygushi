from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
with open('requirements.txt', 'r', encoding='utf-8') as f:
    install_requires = f.read().split('\n')

setup(
    name='pygushi',
    version='1.2.0',
    packages=['pygushi'],
    url='https://github.com/stripepython/pygushi',
    download_url='https://github.com/stripepython/pygushi',
    license='Apache License',
    author='stripe-python',
    author_email='stripe-python@139.com',
    maintainer='stripe-python',
    maintainer_email='stripe-python@139.com',
    description='一个关于爬取古诗文的Python3 API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    python_requires='>=3.7'
)
