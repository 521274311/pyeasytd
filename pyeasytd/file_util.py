import os
from .__init__ import *
from .entries.file.xlsx_file_easy import XlsxFileEasyEntry

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

class XlsxFileUtil:

    @staticmethod
    def create(filepath, default_sheet=None):
        '''
        装载xlsx数据，获取XlsxFileEeasyEntry对象
        :param filepath: 文件相对路径/绝对路径
        :param default_sheet: sheet名或sheet索引，默认sheet，初始化设置默认sheet后续操作可不设置sheet。
        :return: XlsxFileEeasyEntry对象
        '''
        return XlsxFileEasyEntry(filepath, default_sheet)

    @staticmethod
    def rows(obj: XlsxFileEasyEntry, sheet=None):
        '''
        获取行数
        :param obj: XlsxFileEasyEntry对象，可通过XlsxFileUtil.create获取
        :param sheet: xlsx 查询的sheet名或sheet索引
        :return: int
        '''
        return obj.rows(sheet)

    @staticmethod
    def cols(obj: XlsxFileEasyEntry, sheet=None):
        '''
        获取列数
        :param obj: XlsxFileEasyEntry对象，可通过XlsxFileUtil.create获取
        :param sheet: xlsx 查询的sheet名或sheet索引
        :return: int
        '''
        return obj.cols(sheet)

    @staticmethod
    def find(obj: XlsxFileEasyEntry, sheet=None, start_row=None, start_col=None, end_row=None, end_col=None):
        '''
        基于位置查找xlsx文件中的内容
        支持单行查找：start_row=number, 单列查找：start_col=number，返回list
        支持指定元素查找：start_row=number1, start_col=number2，返回str
        支持范围查找：start_row=number1, start_col=number2, end_row=number3, end_col=number4, 返回list[list]
        其中参数要求：
        start_row 与 start_col 不能同时为空
        end_row 不为空时 start_row 也不能为空
        end_col 不为空时 start_col 也不能为空
        :param sheet: sheet名，值为None时使用默认sheet名
        :param start_row: 开始行数，0开始
        :param start_col: 开始列数，0开始
        :param end_row: 结束行数，1开始
        :param end_col: 结束列数，1开始
        :return: list 或 str
        '''
        if BasicCheckUtil.is_none(start_row) and BasicCheckUtil.is_none(start_col):
            raise ValueError('start_row 与 start_col 不能同时为空')
        return obj.find(sheet, start_row, start_col, end_row, end_col)

    @staticmethod
    def sheet_names(obj: XlsxFileEasyEntry):
        '''
        获取所有的sheet名
        :return:
        '''
        return obj.sheets()