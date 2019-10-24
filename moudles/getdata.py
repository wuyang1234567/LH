import json
import math
import os
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
    data = dic
    return data
# 文件单位的函数
def getsize(size, format = 'kb'):
    p = 0
    if format == 'kb':
        p = 1
    elif format == 'mb':
        p = 2
    elif format == 'gb':
        p = 3
    size /= math.pow(1024, p)
    return "%0.2f"%size
def creatdir(dir):
    getaddress=os.path.join(os.getcwd(),dir)
    if os.path.exists(getaddress):    #判断文件 / 文件夹是否存在
        pass
    else:
        dirall=dir.split("/")
        for item,name in enumerate(dirall):
            makedir = os.path.join(os.getcwd(), name)
            # 如果不存在然后添加
            if not os.path.exists(makedir):
                os.mkdir(makedir)
            if item<len(dirall)-1:
                dirall[item+1]=name+"/"+dirall[item+1]
def paging(page,pages):
    '''

    :param page: 当前页数
    :param pages: 总页数
    :return:  "startnum"每屏显示的第一个页数
                "endnum":每屏显示的最后一个页数
    '''
    everypagecount = 3#每屏显示的页数
    changepage = everypagecount / 2#中间的页数
    # 如果总页数小于everypagecount
    if page < changepage:
        startnum = 1
        endnum = everypagecount
    else:
        startnum = math.ceil(page - changepage)
        endnum = math.ceil(page + changepage) - 1
    if endnum > pages:
        endnum = pages
        startnum = endnum - (everypagecount - 1)
    if startnum < 1:
        startnum = 1
        endnum = startnum + everypagecount - 1
        if endnum >= pages:
            endnum = pages
    return{
        "startnum":startnum,
        "endnum":endnum+1
    }