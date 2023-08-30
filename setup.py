from setuptools import setup, find_packages
import re
import os


def get_version():
    fn = os.path.join(os.path.dirname(__file__),
                      "scrapy_proxy_pool", "__init__.py")
    with open(fn) as f:
        return re.findall("__version__ = '([\d.\w]+)'", f.read())[0]


def get_long_description():
    readme = open('README.md').read()


setup(
    name='scrapy-proxy-pool',
    version=get_version(),
    author='Rustam Rasimovich',
    author_email='NoCringe@cringe.dm',
    license='MIT',
    long_description=get_long_description(),
    description="Simple scrapy proxy pool",
    url='https://github.com/ruvn-1fgas/scrapy-proxy-pool',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'scrapy',
        'proxyscrape'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Framework :: Scrapy',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
