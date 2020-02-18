from ..__init__ import *
def send_message_to_enterprise_wechat(url, message='', message_type='text', mentioned_list=None, mentioned_mobile_list=None):
    '''
    todo 企业微信推送信息函数 (单图片发送功能尚未实现)
    当 message_type = text or markdown, message 值为字符串;
    当 message_type = image; message 值为图片二进制数组
    当 message_type = news, message 值为列表, 列表长度 <= 8, 列表里每个元素如下：
        {
            "title": "这是标题, 必填项, 不超过128字节, 超过会自动截断",
            "description": "这是描述, 非必填, 不超过512个字节, 超过会自动截断",
            "url": "这是点击跳转的链接, 必填",
            "picurl": "这是图片链接, 非必填, 支持JPG、PNG格式, 较好的效果为大图 1068*455, 小图150*150"
        }

    mentioned_list 与 mentioned_mobile_list 仅 message_type = text 时生效
    :param url: 企业微信调用url
    :param message: 推送信息内容
    :param message_type: 推送信息类型,仅限 text文本, markdown, image图片, news图文组合信息
    :param mentioned_list: userid的列表, 提醒群中的指定成员(@某个成员), @all表示提醒所有人, 如果不知道userid可以使用mentioned_mobile_list
    :param mentioned_mobile_list: 手机号列表,提醒手机号对应的群成员(@某个成员), @all表示提醒所有人
    :return: requests.Response 对象
    '''
    import requests
    if type(message) in (dict,):
        res = requests.post(url, json=message)
        return res
    elif type(message_type) in (str, bytearray, bytes, list):
        send_data = {}
        send_data['msgtype'] = message_type
        send_data[message_type] = {}
        if BasicCheckUtil.contains(('text', 'markdown'), message_type):
            send_data[message_type]['content'] = message
        elif BasicCheckUtil.equels('image', message_type):
            import base64
            import hashlib
            send_data[message_type]['base64'] = base64.encodebytes(message).decode('utf-8')
            send_data[message_type]['md5'] = hashlib.md5(message).hexdigest()
            print(send_data[message_type]['base64'])
        elif BasicCheckUtil.equels('news', message_type):
            send_data[message_type]['articles'] = message
        if BasicCheckUtil.non_none(mentioned_list):
            send_data[message_type]['mentioned_list'] = __check_list(data_list=mentioned_list)
        if BasicCheckUtil.non_none(mentioned_mobile_list):
            send_data[message_type]['mentioned_mobile_list'] = __check_list(data_list=mentioned_mobile_list)
        res = requests.post(url, json=send_data)
        return res

def __check_list(data_list):
    if type(data_list) in (str,):
        return [data_list]
    return data_list

