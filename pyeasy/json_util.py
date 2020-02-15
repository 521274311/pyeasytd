from .entries.json_easy import JsonEasyEntry
from .__init__ import BasicCheckUtil
import json

class JsonUtil:
    '''
    JsonEasyEntry 简单操作工具类（建议使用）
    使用前建议先调用JsonUtil.print方法查看处理后的json串，便于快捷提取所需数据
    '''
    @staticmethod
    def loads(data: str or dict or list or tuple):
        '''
        装载json数据，获取JsonEeasyEntry对象
        :param data: json结构的字符串或dict对象或列表
        :return: JsonEeasyEntry
        '''
        return JsonEasyEntry(data)

    @staticmethod
    def get_json(obj: JsonEasyEntry):
        '''
        获取json对象
        :param obj: JsonEasyEntry 对象，通过JsonUtil.loads获取
        :return: dict 或 list
        '''
        JsonUtil.__check(obj)
        return obj.get_original_json()

    @staticmethod
    def get_json_str(obj: JsonEasyEntry):
        '''
        获取json字符串
        :param obj: JsonEasyEntry 对象，通过JsonUtil.loads获取
        :return: str
        '''
        JsonUtil.__check(obj)
        return obj.get_original_json_text()

    @staticmethod
    def get(obj: JsonEasyEntry, key: str, index: int or list=None, level: int=None):
        '''
        查找某个key出现的结果。
        当索引index为None时查找所有结果，返回list对象。
        当索引index为list对象时，返回所有索引index对应位置的值，list对象。
        当索引index为某个具体的数值时，返回单个索引index位置的值。
        :param obj: JsonEasyEntry 对象，通过JsonUtil.loads获取
        :param key: 查找的key
        :param:index: 索引
        :param level: 层级，第一级从0开始，查找指定层级，为None时不限制层级。（当存在不同层级出现相同key时可以使用该字段区分）
        例如： {"he":{"he": "sh"}} 时，不使用level而仅使用key时，将会得到[{"he":"sh"},{"sh"}]结果，具体按照业务场景使用
        :return:list 或 tuper
        '''
        JsonUtil.__check(obj)
        if index == None:
            return obj.get(key)
        elif type(index) in (int,):
            return obj.get_one(key, index)
        elif type(index) in (list,):
            result_list = []
            for one_index in index:
                result_list.append(obj.get_one(one_index))
            return result_list

    @staticmethod
    def print(obj: JsonEasyEntry):
        '''
        查看处理后的json
        :param obj:
        :return:
        '''
        obj.print()

    @staticmethod
    def to_json(s, *, encoding=None, cls=None, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
        '''
        字符串转json, 引用自json.loads方法
        '''
        return json.loads(s, encoding=encoding, cls=cls, object_hook=object_hook, parse_float=parse_float,
                   parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)

    @staticmethod
    def to_str(obj, *, skipkeys=False, ensure_ascii=False, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=None, sort_keys=False, **kw):
        '''
        json转字符串，引用自json.dumps方法
        ensure_ascii 默认改为false
        '''
        return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                          allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default, sort_keys=False, **kw)

    @staticmethod
    def __check(obj, *args, **kwargs):
        if BasicCheckUtil.is_none(obj):
            raise RuntimeError("JsonEasyEntry对象不存在")