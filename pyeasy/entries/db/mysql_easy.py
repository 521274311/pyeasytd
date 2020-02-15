from .__init__ import *
import json


class MysqlEasyEntry:
    '''
    todo 基于PyMysql模块的封装实体，SR1
    '''
    __conn = None

    def __init__(self, host, port, username, password, db=None):
        '''
        创建连接，无返回值，内置保存连接
        :param host: Mysql Host
        :param port: Mysql Port
        :param username: Mysql Username
        :param password: Mysql Password
        :param db: Mysql DataBase Name
        :return:
        '''
        import pymysql
        self.__conn = pymysql.connect(host=host, port=int(port), user=username, password=password, database=db)

    def insert_dict_auto_add_table_and_column(self, table, data, mode='into', value_list_split=',', primary_name='id'):
        '''
        插入单条字典类型，如果表不存在，则创建表，如果表中不包含某个列，将会在最后自动新增一列
        :param table: 表
        :param data: 字典结构数据
        :param mode:模式,into overwrite ignore 等，默认 init（追加）
        :return:
        '''
        self.__check_insert(table, data)
        db_table_inf = table.split('.')
        # 连接时未设置默认数据库，则此处设置默认数据库
        if len(db_table_inf) == 2:
            self.__use_database(db_table_inf[0])
        table = db_table_inf[-1]
        if not self.exists_table(table):
            # 通过数据生成表
            self.__data_generate_table(table, data.copy(), value_list_split, primary_name)

        # 获取表的所有列名
        columns = self.__table_column_names(table)
        # 新数据key与列名集合的差集
        diff_key = data.keys() - columns
        # 差集大于 0 表示有新列需要创建
        if len(diff_key) > 0:
            diff_set = {}
            # 循环插入差集数据
            for k, v in data.items():
                if k in diff_key:
                    diff_set[k] = v
            # python 数据转python数据类型，例如 '这是一个字符串' => str, 200 => int
            diff_set = self.__dict_to_type(diff_set, value_list_split)
            # 批量生成列
            self.__dict_add_column(table, diff_set)
        return self.insert_dict(table, data, mode, value_list_split)

    def insert_dict(self, table, data, mode='into', value_list_split=','):
        '''
        插入单条字典结构数据
        :param table: 表名
        :param data: 字典结构数据
        :param mode: 插入模式，into,overwrite,ignore 等，默认into（追加）
        :param value_list_split: 当data某条数据的某个值为tupper或者list，通过此字段做分隔符转换为字符串
        :return:
        '''
        # 基本检测
        self.__check_insert(table, data)
        self.__check_exists_table(table)
        # 获取连接对象
        conn = self.__conn
        # 获取所有的key
        keys = ",".join(map(lambda x: f'`{x}`', data.keys()))
        # 获取所有的value
        values = self.__check_values([data[key] for key in data.keys()], value_list_split)
        # 构造 sql
        sql = f'insert {mode} `{table}` ({keys}) values({",".join(["%s" for i in range(len(data))])})'
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
        except Exception:
            raise RuntimeError(f"插入数据失败，失败sql：{sql % tuple(values)}")
        cursor.close()

    def insert_dicts(self, table, data, once_length=200, mode='into', values_list_split=','):
        '''
        插入 字典元祖/字典列表 结构数据，形如 ({},{}) 或 [{},{}]，要求每个字典的key全部一致
        :param table: 表名
        :param data: 数据
        :param once_length: 单批插入数据量
        :param mode: 插入模式，into,overwrite,ignore 等，默认into（追加）
        :return:
        '''
        # 基本检测
        self.__check_insert(table, data)
        self.__check_exists_table(table)
        # 获取连接
        conn = self.__conn
        keys = ",".join(map(lambda x: f'`{x}`', data[0].keys()))
        cursor = conn.cursor()
        for i in range(int((len(data) - 1) / once_length) + 1):
            # 分为length批次写入
            length = min(len(data), (i + 1) * once_length)
            sql = f'insert {mode} {table} ({keys}) values '
            values = []
            for dict_obj in data[i * once_length: length]:
                sql += f' ({",".join(["%s" for i in range(len(dict_obj))])}),'
                values += [dict_obj[key] for key in dict_obj.keys()]
            # 剔除末尾空格
            sql = sql[:-1]
            # values 值检测
            values = self.__check_values(values, values_list_split)
            try:
                cursor.execute(sql, values)
            except Exception:
                raise RuntimeError(f"插入数据失败，失败sql：{sql % tuple(values)}")
        conn.commit()
        cursor.close()

    def execute(self, sql):
        '''
        Mysql sql执行方法（不建议使用）
        :param sql: 执行sql
        :return:
        '''
        self.__check_conn()
        if BasicCheckUtil.is_none(sql):
            raise ValueError('sql 不能为空')
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        return self

    def query(self, sql, args=None, type='dict'):
        '''
        Mysql查询方法
        :param sql: 查询sql，传参使用%s代替
        :param args: 参数对象，元组（tuper）或字典（dict）均可
        :param type: 类型，dict返回形如[{'xxx' : 'xxx'},{'xxx' : 'xxx'}]，tuple返回形如((xxx,xx),(xxx,xx))结果
        :return:
        '''
        self.__check_conn()
        if BasicCheckUtil.is_none(sql):
            raise ValueError('sql 不能为空')
        if type not in ('dict', 'tuple'):
            raise TypeError('返回元素子元素类型必须指定为dict或tuple')

        conn = self.__conn
        if type == 'dict':
            from pymysql.cursors import DictCursor
            cursor = conn.cursor(cursor=DictCursor)
        else:
            cursor = conn.cursor()
        cursor.execute(sql, args=args)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        return result

    def insert(self, sql, args=None):
        '''
        todo
        :param sql: sql 字符串
        :param args: 参数元组或列表
        :return:
        '''
        return self.__execute(sql, args, 'insert 失败')

    def update(self, sql, args=None):
        '''
        修改数据
        :param sql: sql 字符串
        :param args: 参数元组或列表
        :return:
        '''
        return self.__execute(sql, args, 'update 失败')

    def delete(self, sql, args=None):
        '''
        删除数据
        :param sql: sql字符串
        :param args: 参数元组或列表
        :return:
        '''
        return self.__execute(sql, args, 'delete 失败')

    def add_column(self, table, name, type):
        '''
        添加一个列
        :param table: 表名
        :param name: 列名
        :param type: python类型
        :return:
        '''
        type = self.__type_to_mysql_type_str(type)
        sql = f'alter table {table} add column {name} {type}'
        self.__execute(sql)

    def close(self):
        '''
        关闭Mysql连接
        :return:
        '''
        self.__conn.close()

    def exists_table(self, table):
        '''
        判断表是否存在
        :param table: 表名
        :return:
        '''
        tables = self.show_tables()
        for tb in tables:
            if table == tb[0]:
                return True
        return False

    def create_table(self, sql, args=None):
        '''
        创建表
        :param sql: sql
        :param args: 参数
        :return:
        '''
        return self.__execute(sql, args)

    def show_tables(self):
        return self.query('show tables', type='tuple')

    def __dict_add_column(self, table, data):
        '''
        字段名， 类型字典
        :param table: 表名
        :param data: {'字段名':类型}
        :return:
        '''
        for k, v in data.items():
            self.add_column(table, k, v)

    def __data_generate_table(self, table, data, split, primary):
        '''
        dict数据生成mysql表
        :param table: 表名
        :param data: dict数据
        :param split:对于tuple，list对象转为str时的分隔符
        :return: None
        '''
        # 将dict数据的value转为数据的类型
        data = self.__dict_to_type(data, split)
        # 存在 id 则删除
        if BasicCheckUtil.non_none(data.get('id')):
            del data['id']
        # 构造sql
        sql = f'create table `{table}` (`{primary}` int(11) not null auto_increment,'
        for k, v in data.items():
            if v in (int, bool):
                sql += f'`{k}` int(11) default null,'
            elif v == float:
                sql += f'`{k}` decimal(16,6) default null,'
            elif v == str:
                sql += f'`{k}` varchar(255) default null,'
            else:
                sql += f'`{k}` varchar(1000) default null,'
        sql += f'primary key(`{primary}`))'
        self.__execute(sql)

    def __use_database(self, database):
        '''
        选择默认数据库
        :param database: 数据库名
        :return:
        '''
        self.__execute(f"use {database}")

    def __execute(self, sql, args=None, error_message='执行失败'):
        '''
        Sql 执行方法（核心方法）
        :param sql: sql字符串
        :return:
        '''
        self.__check_conn()
        if BasicCheckUtil.is_empty(sql):
            raise ValueError('sql 不能为空')
        conn = self.__conn
        cursor = conn.cursor()
        try:
            cursor.execute(sql, args)
            conn.commit()
        except:
            raise RuntimeError(f"{error_message}，失败sql：{sql % (tuple() if args == None else args)}")
        cursor.close()
        return True

    def __dict_to_type(self, data, split):
        '''
        dict结构数据值转为类型
        :param data:
        :return:
        '''
        for key in data.keys():
            data[key] = type(self.__data_to_mysql_data(data[key], split))
        return data

    def __type_to_mysql_type_str(self, type):
        if type in (int, bool):
            return 'int(11)'
        elif type in (float,):
            return 'decimal(16,6)'
        elif type in (str,):
            return 'varchar(255)'
        else:
            return 'varchar(1000)'

    def __data_to_mysql_data(self, data, split):
        '''
        Python 数据类型转 Mysql 数据类型
        :param data:
        :param split:
        :return:
        '''
        if type(data) in (tuple, list):
            return split.join(data)
        if type(data) in (dict,):
            return json.dumps(data, ensure_ascii=False)
        return data

    def __table_column_names(self, table):
        '''
        获取表的所有列
        :param table: 表名
        :return:
        '''
        self.__check_conn()
        conn = self.__conn
        cursor = conn.cursor()
        cursor.execute(f'select * from {table} limit 1')
        columns = [column[0] for column in cursor.description]
        cursor.close()
        return columns

    def __check_values(self, values, split):
        '''
        values 参数检测
        :return:
        '''
        for index in range(len(values)):
            values[index] = self.__data_to_mysql_data(values[index], split)
        return values

    def __check_insert(self, table, data):
        self.__check_conn()
        if BasicCheckUtil.is_empty(table):
            raise ValueError('表名不能为空')
        if BasicCheckUtil.is_empty(data):
            raise ValueError('数据不能为空')

    def __check_conn(self):
        '''
        检测是否存在Mysql连接
        :return:
        '''
        if BasicCheckUtil.is_none(self.__conn):
            raise ConnectionError('当前没有Mysql可用连接对象')

    def __check_exists_table(self, table):
        if self.exists_table(table) == False:
            raise EOFError(f"未找到表 {table}")