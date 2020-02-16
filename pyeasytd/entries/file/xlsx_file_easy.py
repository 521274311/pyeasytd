import os
import xlrd
from .__init__ import *

class XlsxFileEasyEntry:
    '''
    todo 基于 xlrd 模块的简单封装，简化 xlrd 操作
    '''
    __file_path = None
    __book = None # 工作簿对象
    __sheet_names = []
    __sheet = {} # sheet对象存储
    __sheet_dis = {} # sheet解析后存储
    __rows = {} # 行数存储字典
    __cols = {} # 列数存储字典
    __default_sheel_key = None
    def __init__(self, path: str, default_sheet=None):
        self.__check(path)
        self.__file_path = os.path.abspath(path)
        self.__init_book()
        if BasicCheckUtil.non_none(default_sheet):
            if type(default_sheet) in (str, int):
                self.__init_sheet(sheet=default_sheet)
            elif type(default_sheet) in (list, tuple):
                for st in default_sheet:
                    self.__init_sheet(sheet=st)


    def find(self, sheet=None, start_row=None, start_col=None, end_row=None, end_col=None):
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
        if BasicCheckUtil.is_empty(sheet):
            self.__check_sheet(self.__default_sheel_key)
            local_sheet_key = self.__default_sheel_key
        else:
            self.__init_sheet(sheet=sheet)
            self.__check_sheet(sheet)
            local_sheet_key = sheet
        result_list = []
        if BasicCheckUtil.is_none(start_row) and BasicCheckUtil.is_none(start_col):
            raise ValueError('start_row 与 start_col 不能同时为空')
        if BasicCheckUtil.is_none(start_col):
            if BasicCheckUtil.is_none(end_row):
                result_list = self.__rows[local_sheet_key][start_row]
            else:
                for index in range(start_row, end_row):
                    result_list.append(self.__rows[local_sheet_key][index])
        elif BasicCheckUtil.is_none(start_row):
            if BasicCheckUtil.is_none(end_col):
                result_list = self.__cols[local_sheet_key][start_col]
            else:
                for index in range(start_col, end_col):
                    result_list.append(self.__cols[local_sheet_key][index])
        else:
            if not ((BasicCheckUtil.is_none(end_col) and BasicCheckUtil.is_none(end_row))
                    or (BasicCheckUtil.non_none(end_col) and BasicCheckUtil.non_none(end_row))):
                raise ValueError('当start_row 与 start_col 同时存在值时，end_row 与 end_col 必须同时存在值或同时为 None')
            if BasicCheckUtil.is_none(end_col) and BasicCheckUtil.is_none(end_row):
                result_list = self.__rows[local_sheet_key][start_row][start_col]
            else:
                for index in range(start_row, end_row):
                    result_list.append(self.__rows[local_sheet_key][index][start_col:end_col])
        return result_list

    def rows(self, sheet=None):
        '''
        获取行数
        :param sheet: 对应的xlsx的sheet名，当为None时使用默认的sheet名
        :return:
        '''
        if BasicCheckUtil.is_empty(sheet):
            self.__check_sheet(self.__default_sheel_key)
            return len(self.__rows[self.__default_sheel_key])
        else:
            self.__init_sheet(sheet=sheet)
            self.__check_sheet(sheet)
            return len(self.__rows[sheet])

    def cols(self, sheet=None):
        '''
        获取列数
        :param sheet: 对应的xlsx的sheet名，当为None时使用默认的sheet名
        :return:
        '''
        if BasicCheckUtil.is_empty(sheet):
            self.__check_sheet(self.__default_sheel_key)
            return len(self.__cols[self.__default_sheel_key])
        else:
            self.__init_sheet(sheet=sheet)
            self.__check_sheet(sheet)
            return len(self.__cols[sheet])

    def sheets(self):
        self.__init_book()
        return self.__sheet_names

    def __init_sheet(self, **kwargs):
        for key, value in kwargs.items():
            value_str = str(value)
            if BasicCheckUtil.equels(key, 'sheet') and BasicCheckUtil.is_none(self.__sheet.get(value_str)):
                if type(value) in (int,):
                    self.__sheet[value_str] = self.__book.sheet_by_index(value)
                elif type(value) in (str,):
                    self.__sheet[value_str] = self.__book.sheet_by_name(value)
                if BasicCheckUtil.is_none(self.__default_sheel_key):
                    self.__default_sheel_key = value_str
                self.__rows[value_str] = []
                self.__cols[value_str] = []
                for row_index in range(self.__sheet[value_str].nrows):
                    self.__rows[value_str].append(self.__sheet[value_str].row_values(row_index))
                for col_index in range(self.__sheet[value_str].ncols):
                    self.__cols[value_str].append(self.__sheet[value_str].col_values(col_index))

    def __init_book(self):
        if BasicCheckUtil.is_none(self.__book):
            self.__book = xlrd.open_workbook(self.__file_path)
            self.__sheet_names = self.__book.sheet_names()

    def __check(self, path):
        if BasicCheckUtil.is_empty(path):
            raise ValueError('文件路径不能为空')

    def __check_sheet(self, sheet_key):
        if BasicCheckUtil.is_none(self.__sheet.get(sheet_key)):
            raise ValueError('没有指定的sheet对象')