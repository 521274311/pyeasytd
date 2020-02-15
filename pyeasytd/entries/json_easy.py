from .__init__ import *

class JsonEasyEntry:
    '''
    基于json模型封装实体，适用于规则的多层嵌套json读取
    '''
    __level_prefix = 'level_'
    __init_load_status = False
    __json = None
    __json_text = None
    __struct = {}
    __count = {}

    def __init__(self, data: str or dict or list or bytes or bytearray):
        import json
        if type(data) in (str,):
            self.__json = json.loads(data)
            self.__json_text = data
        elif type(data) in (dict, list, tuple):
            self.__json = data
            self.__json_text = json.dumps(data)

    def print(self):
        '''
        输出包含所有结构的json
        :return:
        '''
        import json
        self.__init_load()
        print(json.dumps(self.__struct))

    def get(self, key, level: int=None):
        '''
        获取某个key的结果
        :param key: 字典的key
        :param level: 层级，第一级从0开始，查找指定层级，为None时不限制层级
        :return: list，对应key的结果列表（可能包含多个同名key）
        '''
        self.__init_load()
        if BasicCheckUtil.is_none(level):
            result_list = []
            for level_key, value in self.__struct.items():
                if BasicCheckUtil.non_none(value.get(key)):
                    result_list += value[key]
            return result_list
        level_key = self.__level_prefix + str(level)
        return self.__struct[level_key][key]

    def get_first(self, key, level: int=None):
        '''
        获取某个key的第一个结果
        :param key: 字典的key
        :param level: 层级，第一级从0开始，查找指定层级，为None时不限制层级
        :return: list的第一个元素
        '''
        return self.get_one(key, 0, level)

    def get_last(self, key, level: int=None):
        '''
        获取某个key的最后一个结果
        :param key: 字典的key
        :param level: 层级，第一级从0开始，查找指定层级，为None时不限制层级
        :return: list的最后一个元素
        '''
        if BasicCheckUtil.is_none(level):
            total = 0
            for level_key, value in self.__count.items():
                if BasicCheckUtil.non_none(value.get(key)):
                    total += value[key]
            return self.get_one(key, total - 1, level)
        level_key = self.__level_prefix + str(level)
        return self.get_one(key, self.__count[level_key][key] - 1, level)


    def get_one(self, key, index=0, level: int=None):
        '''
        获取某个key的指定位置结果
        :param key: 字典的key
        :param index: 第 index 次出现
        :param level: 层级，第一级从0开始，查找指定层级，为None时不限制层级
        :return: list 的第 index个元素，从0开始
        '''
        self.__init_load()
        if BasicCheckUtil.is_none(level):
            result_list = []
            for level_key, value in self.__struct.items():
                if BasicCheckUtil.non_none(value.get(key)):
                    result_list += value[key]
                    if len(result_list) > index:
                        return result_list[index]
            return result_list[index]
        level_key = self.__level_prefix + str(level)
        return self.__struct[level_key][key][index]

    def get_original_json(self):
        '''
        获取原始传入dict对象
        :return:dict
        '''
        return self.__json

    def get_original_json_text(self):
        '''
        获取原始传入json字符串
        :return: str
        '''
        return self.__json_text

    def __init_load(self):
        '''
        装载dict对象
        :return:
        '''
        if not self.__init_load_status:
            if self.__json is None:
                return ValueError('当前没有Json对象')
            self.__re_init_load(self.__json)
            self.__init_load_status = True

    def __re_init_load(self, param, level=0):
        '''
        提取嵌套dict至最外层
        :param param:
        :return:
        '''
        level_key = self.__level_prefix + str(level)
        if BasicCheckUtil.is_none(self.__struct.get(level_key)):
            self.__struct[level_key] = {}
            self.__count[level_key] = {}
        if type(param) in (dict,):
            for key, value in param.items():
                count = self.__count[level_key].get(key)
                if count is None:
                    count = 0
                    self.__struct[level_key][key] = []
                self.__struct[level_key][key].insert(count, value)
                count += 1
                self.__count[level_key][key] = count
                self.__re_init_load(value, level + 1)
        elif type(param) in (list, tuple):
            for single in param:
                self.__re_init_load(single, level + 1)
