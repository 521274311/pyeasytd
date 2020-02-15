
class BasicCheckUtil:
    '''
    todo 基本数据类型检测工具类
    '''
    @classmethod
    def is_empty(cls, param):
        '''
        todo 判断对象是否为空，添加对基本数据类型的检测
        :param param: 参数
        :return:
        '''
        if cls.is_none(param):
            return True
        if type(param) in (int,float) and param == 0:
            return True
        if type(param) in (str,) and param == '':
            return True
        if type(param) in (tuple, list, dict) and len(param) == 0:
            return True
        if type(param) in (bool,) and param == False:
            return True
        return False

    @classmethod
    def non_empty(cls, param):
        '''
        todo 判断对象是否非空，添加对基本数据类型的检测
        :param param: 参数
        :return:
        '''
        return not cls.is_empty(param)

    @classmethod
    def is_none(cls, param):
        '''
        todo 判断对象是否为空
        :param param: 参数
        :return:
        '''
        if param is None:
            return True
        return False

    @classmethod
    def non_none(cls, param):
        '''
        todo 判断对象是否非空
        :param param: 参数
        :return:
        '''
        return not cls.is_none(param)
