import os
from .__init__ import *

class FileUtil:
    '''
    文件操作工具类
    '''
    @staticmethod
    def file_create(path):
        '''
        创建文件，支持多级目录嵌套创建
        :param path: 文件相对路径/绝对路径
        :return:
        '''
        FileUtil.__check(path)
        # win 分隔符替换
        path = path.replace(r'\\', '/')
        with open(path) as f:
            pass
        return True

    @staticmethod
    def file_remove(path):
        '''
        删除文件
        :param path: 文件相对路径/绝对路径
        :return:
        '''
        FileUtil.__check(path)
        return os.remove(path)
    
    @staticmethod
    def file_read(file, buffering=8192, encoding='utf-8', errors=None, newline=None, closefd=True):
        '''
        文件读取,引用自内置函数open,对应open().read()方法
        调整encoding默认编码为utf-8
        '''
        if FileUtil.file_exists(file):
            with open(file, mode='r', buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd) as f:
                return f.read()

    @staticmethod
    def file_readlines(file, buffering=8192, encoding='utf-8', errors=None, newline=None, closefd=True):
        '''
        文件读取,引用自内置函数open,对应open().readlines()方法
        调整encoding默认编码为utf-8
        '''
        if FileUtil.file_exists(file):
            with open(file, mode='r', buffering=buffering, encoding=encoding, errors=errors, newline=newline,
                      closefd=closefd) as f:
                return f.readlines()

    @staticmethod
    def file_exists(path):
        '''
        检测文件是否存在
        :param file_path: 文件相对路径/绝对路径
        :return:
        '''
        FileUtil.__check(path)
        return FileUtil.__exists(path) and os.path.isfile(path)

    @staticmethod
    def dir_create(path):
        '''
        创建目录，支持多级目录嵌套创建
        :param path: 目录相对路径/绝对路径
        :return:
        '''
        FileUtil.__check(path)
        if not FileUtil.__exists(path):
            os.makedirs(path)
        return True
    
    @staticmethod
    def dir_remove(path):
        '''
        删除目录，支持非空目录删除
        :param path: 目录相对路径/绝对路径
        :return: 
        '''
        import shutil
        shutil.rmtree(path)
        return True

    @staticmethod
    def dir_exists(path):
        '''
        检测目录是否存在
        :param dir_path: 目录相对路径/绝对路径
        :return:
        '''
        FileUtil.__check(path)
        return FileUtil.__exists(path) and os.path.isdir(path)

    @staticmethod
    def dir_or_file_exists(path):
        '''
        检测路径是文件或目录
        :param path: 相对路径/绝对路径
        :return:
        '''
        FileUtil.__check(path)
        return FileUtil.__exists(path)

    @staticmethod
    def __exists(path):
        '''
        检测目录/文件是否存在
        :param path: 目录/文件 相对路径/绝对路径
        :return:
        '''
        FileUtil.__check(path)
        return os.path.exists(path)

    @staticmethod
    def __check(path, *args, **kwargs):
        '''
        路径检测
        :param path: 相对路径/绝对路径
        :return:
        '''
        if BasicCheckUtil.is_empty(path):
            raise ValueError('路径不能为空')