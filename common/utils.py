import  json
# 封装返回数据的方法
import math
import os
from cms import settings

# def returnResult(code,msg,data=""):
#     returndata={
#         "code":code,
#         "msg":msg,
#         "data":data
#     }
#     returndata1=json.dumps(returndata)
#     return returndata1


def returnResult(code,msg,data=""):
    returndata={
        "code":code,
        "msg":msg,
        "data":data
    }
    return returndata

def getsize(size, format = 'kb'):
    '''
    此方法用于判断文件图片的大小
    :param data:
    :return:
    '''
    p = 0
    if format == 'kb':
        p = 1
    elif format == 'mb':
        p = 2
    elif format == 'gb':
        p = 3
    size /= math.pow(1024, p)
    return "%0.2f"%size
def creatDir(path):
    dirlist=path.split("/")
    # print(dirlist)
    for i,name in enumerate(dirlist):
        # print(i,"===",name)
        item=name
        itemdir=os.path.join(os.getcwd(),item)
        # print(itemdir)
        # 遍历完以后先看第一层文件夹是否存在，存在的话看里面还有没有路径，
        # 没有的话就在这个文件夹储存，有的话就把索引值1的跟当前这个拼接上
        if not os.path.exists(itemdir):
            os.mkdir(itemdir)
        if i<len(dirlist)-1:
            # 说明后面还有文件夹需要创建
            dirlist[i+1]=itemdir+"/"+dirlist[i+1]

def getViewPage(allPage,currentPage):
    '''

    :param allPage: 总页数
    :param currentPage: 当前的页码
    :return:
    '''
    # return 1
    nowpage=currentPage
    everyPageButton = 3  # 规定的每页按钮数
    middle = everyPageButton / 2
    if int(nowpage) <= middle + 1:
        start=0
        end=everyPageButton
    elif int(nowpage) >= allPage - middle:
        start=allPage - everyPageButton
        end=allPage
    else:
        start=int(nowpage) - math.floor(middle) - 1
        end=int(nowpage) + math.floor(middle)
    if (end > allPage):  # 3>2
        end = allPage
    pageList=range(start,end)
    allpageList = []
    for i in pageList:
        allpageList.append(i + 1)
    return allpageList