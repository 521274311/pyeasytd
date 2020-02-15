from .entries.db.mysql_easy import MysqlEasyEntry
from .__init__ import BasicCheckUtil

class MysqlUtil:
    '''
    MysqlEasyEntry 简单操作工具类（建议使用）
    '''
    @staticmethod
    def connect(host, port, username, password, db=None):
        '''
        获取Mysql连接封装对象
        :param host: Mysql Host
        :param port: Mysql Port
        :param username: Mysql Username
        :param password: Mysql Password
        :param db: Mysql DataBase Name
        :return:MysqlEasyEntry
        '''
        return MysqlEasyEntry(host, port, username, password, db)

    @staticmethod
    def insert_dict(obj: MysqlEasyEntry, table: str, data: dict, mode='into'):
        '''
        插入数据
        :param obj: MysqlEasyEntry对象，通过MysqlUtil.connect获取
        :param table: 表名
        :param data: 字典结构数据,key 与 mysql 字段一一对应
        :param mode: 插入模式，包括 into(追加)，overwrite(覆盖)，ignore(忽略) 等
        :return: None.
        '''
        MysqlUtil.__check(obj)
        obj.insert_dict(table, data, mode)

    @staticmethod
    def insert_dicts(obj: MysqlEasyEntry, table: str, data: tuple or list, mode='into', every_length=200):
        '''
        批量插入数据
        :param obj: MysqlEasyEntry对象，通过MysqlUtil.connect获取
        :param table: 表名
        :param data: tuper或list类型，其中每个元素为dict类型
        :param mode: 插入模式，包括 into(追加)，overwrite(覆盖)，ignore(忽略) 等
        :param every_length: 分批插入的单批条数，例如：len(data)=1000，every_length=200，则会将数据分为5批，每批以200条数据插入
        :return: None.
        '''
        MysqlUtil.__check(obj)
        obj.insert_dicts(table, data, every_length, mode)

    @staticmethod
    def insert_dict_auto_create_table_and_column(obj: MysqlEasyEntry, table: str, data: dict, mode='into', primary_name='id'):
        '''
        插入单条字典类型，如果表不存在，则创建表，如果表中不包含某个列，将会在最后自动新增一列
        :param obj: MysqlEasyEntry对象，通过MysqlUtil.connect获取
        :param table: 表名
        :param data: dict类型
        :param mode: 插入模式，包括 into(追加)，overwrite(覆盖)，ignore(忽略) 等
        :param primary_name: 主键
        :return:
        '''
        MysqlUtil.__check(obj)
        obj.insert_dict_auto_add_table_and_column(table, data, mode, primary_name=primary_name)

    @staticmethod
    def update(obj: MysqlEasyEntry, sql, args=None):
        '''
        更新数据
        :param obj: MysqlEasyEntry对象，通过MysqlUtil.connect获取
        :param sql: 更新的sql
        :param args: 参数元组或列表
        :return: None.
        '''
        MysqlUtil.__check(obj)
        obj.update(sql, args)

    @staticmethod
    def query(obj: MysqlEasyEntry, sql, args=None, data_type='dict'):
        '''
        查询数据
        :param obj: MysqlEasyEntry对象，通过MysqlUtil.connect获取
        :param sql: 查询的sql
        :param args: 参数元组或列表
        :param data_type: 单元素类型，dict 或 tuper
        :return:tuper
        '''
        MysqlUtil.__check(obj)
        return obj.query(sql, args, data_type)

    @staticmethod
    def delete(obj: MysqlEasyEntry, sql, args=None):
        '''
        删除数据
        :param obj: MysqlEasyEntry对象，通过MysqlUtil.connect获取
        :param sql: 删除的sql
        :param args: 参数元组或列表
        :return: None.
        '''
        MysqlUtil.__check(obj)
        return obj.delete(sql, args)

    @staticmethod
    def __check(obj, *args, **kwargs):
        if BasicCheckUtil.is_none(obj):
            raise RuntimeError("MysqlEasyEntry对象不存在")