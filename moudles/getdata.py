import json
def returnmsg(code,message,elsemsg=""):
    '''
    :param code: 0代表成功
    :param message: 返回的信息
    :param elsemsg: 其他信息
    :return:
    '''
    dic = {
        'code': code,
        'message': message,
        "elsemsg":elsemsg
    }
    data = json.dumps(dic)
    return data