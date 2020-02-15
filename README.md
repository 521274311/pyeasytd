## pyeasy 使Python开发变的更简单  
版本变更内容：  
1.新增MysqlEasyEntry,JsonEasyEntry对象  
2.新增MysqlUtil,JsonUtil工具类  

使用实例：
1.MysqlUtil  
from pyeasy.mysql_util import MysqlUtil  
obj = MysqlUtil.connect(...)  
MysqlUtil.xxx(obj, ...)  
2.JsonUtil  
from pyeasy.json_util import JsonUtil  
obj = JsonUtil.loads(...)  
JsonUtil.xxx(obj, ...)  