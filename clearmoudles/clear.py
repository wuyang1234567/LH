from server.models import *
import os
from datetime import datetime
import re
def clearimg():
    # 清理用户管理里面的无用图片
    userall=admin.objects.all()
    # 删除缩略图中无用的图片
    newsall=news.objects.all()
    newlist=[]
    for item in newsall:
        newlist.append(item.thumb)
    userlist=[]
    for item in userall:
        userlist.append(item.heading)
    newlist.extend(userlist)
    uploadsimg=os.listdir(os.path.join(os.getcwd(),"static/uploads"))
    diffimg=list(filter(lambda x: x not in newlist, uploadsimg))
    if len(diffimg)!=0:
        for item in diffimg:
            os.remove("static/uploads/"+item)
    # 清理富文本编辑器里的无用图片
    imagesimg=os.listdir(os.path.join(os.getcwd(),"static/images"))
    content=news_content.objects.all()
    newcontentlist = []
    for item in content:
        content=item.content
        reg = '<img.*?src="/static/images/(.*?)".*?/>'
        m = re.findall(reg, content)
        if m !=[]:
            newcontentlist.extend(m)
    diffimages = list(filter(lambda x: x not in newcontentlist, imagesimg))
    if len(diffimages) != 0:
        for item in diffimages:
            os.remove("static/images/" + item)


