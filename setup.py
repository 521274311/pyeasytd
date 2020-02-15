try:
    from setuptools import setup
except:
    from distutils.core import setup
import setuptools

setup(
    name='pyeasytd',
    author='dragons',
    version='0.0.1',
    description='使Python开发变的更简单',
    long_description='Python 简化处理工具，轻松、快捷编码，使Python开发变的更简单。',
    author_email='521274311@qq.com',
    url='https://gitee.com/kingons/pyeasytd-black-unique.git',
    packages=setuptools.find_packages(),
    install_requires= [
        # 'fake-useragent>=0.1.11',
        'PyMySQL>=0.9.3',
        # 'numpy>=1.17.4',
        # 'moviepy>=1.0.1',
        # 'Pillow>=6.2.1',
        # 'requests>=2.22.0',
        # 'urllib3>=1.25.7',
        # 'bs4>=0.0.1',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=True,
)