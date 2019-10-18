import math
import os
import re

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from server.models import *
from moudles import getdata
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
from  datetime import datetime
from common import utils
from django.shortcuts import redirect
from cms import settings
import json
from django.core.paginator import Paginator

class TestUEditorForm(forms.Form):
    content = UEditorField('', width=800, height=300, toolbars="full", imagePath="static/uploads/", filePath="static/files/",
      upload_settings={"imageMaxSize":1204000},
      settings={})
def index(request):
    newscount=news.objects.all()
    newsnum = news.objects.values("num").order_by("-num")
    count=newscount.count()
    name = request.session.get('username')
    # print(name)
    # if name:
    positioncontent = position_content.objects.all()
    positioncount = positioncontent.count()
    context = {
        "count": count,
        "name": name,
        "maxnum": newsnum[0]["num"],
        "positioncount": positioncount
    }
    return render(request, "temp-server/index.html", context)
    # else:
    #     print("session里面没有用户名")
    #     return redirect("/server/login")
def login(request):
    print("进了login")
    return render(request,"temp-server/login.html")
def loginHandler(request):
    print("进了loginhandler")
    username=request.POST.get("username")
    password=request.POST.get("password")
    email=request.POST.get("email")
    request.session['username'] = username
    # print(username)
    namelist=admin.objects.filter(username=username).all()
    print(namelist)
    if namelist:
        for item in namelist:
            if item.username==username:
                # print("999")
                if item.password==password:
                    return JsonResponse(utils.returnResult("0", "登录成功", ""))
                else:
                    return JsonResponse(utils.returnResult("1", "密码不正确", ""))
    return JsonResponse(utils.returnResult("2", "用户名不存在", ""))
def  quitlogin(request):
    del request.session["username"]
    return redirect("/server/login")
def menus(request):
    name = request.session.get('username')
    # print(name)
    if name:
        menulist = menu.objects.all()
        context={
            "menulist":menulist
        }
        print(context)
        return render(request,"temp-server/menu.html",context)
    else:
        return redirect("/server/login")
def addmenu(request):
    return render(request,"temp-server/addmenu.html")
def addmenuHandler(request):
    menuname=request.POST.get("menuname")
    name=menu(name=menuname)
    name.save()
    # print("9999999999999999")
    return JsonResponse(utils.returnResult("0", "增加成功", ""))
def editmenu(request):
    id=request.GET.get("id")
    # print(id)
    menuname = menu.objects.filter(id=id).get()
    context = {
        "name": menuname
    }
    return render(request, "temp-server/editmenu.html", context)
def editmenuHandler(request):
    id = request.POST.get("id")
    # print(id)
    newname = request.POST.get("menutitle")
    menu.objects.filter(id=id).update(name=newname)
    return JsonResponse(getdata.returnmsg("0", "提交成功", ""))
def deletemenu(request):
    '''
    删除菜单的方法
    :param request:
    :return:
    '''
    menuid = request.GET.get("menuid")
    try:
        menu.objects.filter(id=menuid).delete()
        return JsonResponse(utils.returnResult(0, "删除成功"))
    except Exception as e:
        return JsonResponse(utils.returnResult(1, "删除失败"))
def articlelist(request):
    # 先对地址中是否有页码进行判断
    nowpage=1            #没有传递page参数
    if request.GET.get("page"):        #如果地址中有页数
        nowpage = request.GET.get("page")
    # 先对地址中是否有catid进行判断
    catId = -1  # 想读取所有分类
    if request.GET.get("catId"):  # 如果地址中有catid
        catId = int(request.GET.get("catId"))
    # print(int(catId))
    # 先对地址中是否有keytitle进行判断
    keytitle = ""  # 想读取所有分类
    if request.GET.get("keytitle"):  # 如果地址中有catid
        keytitle = request.GET.get("keytitle")
    if catId == -1:
        allresult = news.objects.filter(title__contains=keytitle).order_by("-lasttime")
    else:
        allresult = news.objects.filter(catid=catId,title__contains=keytitle).order_by("-lasttime")
    menulist = menu.objects.all()

    everyPageCount=2  # 规定的每页显示几条文章
    allcount=len(allresult)         #总条数
    allpagesCount=math.ceil(allcount/everyPageCount)       #一共几页
    allpageList=utils.getViewPage(allpagesCount,nowpage)
    beginsuo=settings.PAGES["everyCount"]*int(nowpage)-settings.PAGES["everyCount"]    #这个页面显示的列表的开始的索引值
    result=allresult[beginsuo:beginsuo+settings.PAGES["everyCount"]]
    # 以下是在解决列表页面显示栏目而非id的问题，并且不用每次都从数据中读，先过滤！！
    for item in result:
        catid=item.catid
        result1=filter(lambda x:x.id==catid,menulist)
        catlisttemp=list(result1)
        if catlisttemp:
            item.lanmu=catlisttemp[0].name
    # print(int(nowpage))
    # print(allpageList)
    # 关于推荐位
    positionlist=position.objects.all()
    # print(positionlist)
    return render(request, "temp-server/articlelist.html",{"articlelist":result,"nowpage":int(nowpage),"allpageList":allpageList,"allpagesCount":allpagesCount,"menulist":menulist,"catId":int(catId),"keytitle":keytitle,"positionlist":positionlist})
def addarticle(request):
    # print("555")
    # 注入富文本编辑器
    form = TestUEditorForm()
    # # 得到所有的栏目
    menuall = menu.objects.all()
    # context={
    #     "msg":menuall,
    #     "form": form,
    # }
    # 注入颜色列表
    # print(settings.COLOR_LIST)
    return render(request,"temp-server/addarticle.html",{"form":form,"colorlist":settings.COLOR_LIST,"menuall":menuall})
def addarticleHandler(request):
    # print("22222")
    '''
    此方法用于处理前端表单传过来的新增加的文章
    :param request:
    :return:
    '''
    title = request.POST.get("title")
    headImg = request.FILES.get("headimg")
    titleColor = request.POST.get("color")
    column = request.POST.get("column")
    content = request.POST.get("content")
    lasttime=datetime.now()
    # print(title,headImg,titleColor,column,content,lasttime)
    # 先判断文件是否存在  存在再判断文件是否符合标准
    # print(titleColor)
    if headImg:
        # print(headImg.name.split(".")[-1])
        if headImg.name.split(".")[1] not in settings.UPLOAD["type"]:
            # print("111")
            return JsonResponse(utils.returnResult(1, "文件类型不正确"))
        imgsize=utils.getsize(headImg.size)
        # print("=====",float(imgsize))
        if float(imgsize)>settings.UPLOAD["unit"]:
            return JsonResponse(utils.returnResult(1, "文件过大"))
        # 走到这里说明文件符合要求，可以储存了
        filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
        # print(filename)
        dir="static/uploads"
        utils.creatDir(dir)
        savePath=dir+"/"+filename
        # print(savePath)
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
        # 写入数据库
        result=news(catid=column,title=title,title_font_color=titleColor,thumb=filename,num=0,lasttime=lasttime)
        result.save()
    else:
        # 没有选择图片进来
        result = news(catid=column, title=title, title_font_color=titleColor, num=0,lasttime=lasttime)
        result.save()
    # 写入文章内容表
    newid=result.id
    # print(newid)
    news_content(newid=newid,content=content).save()
    return JsonResponse(utils.returnResult(0, "增加文章成功"))
def editarticle(request):
    # print("进了editarticle")
    form = TestUEditorForm()
    id = request.GET.get("id")
    # print(id)
    article = news.objects.filter(id=id).get()
    menuall = menu.objects.all()
    content = news_content.objects.filter(newid=id).get()
    return render(request, "temp-server/editarticle.html", {"form":form,"article":article,"colorlist":settings.COLOR_LIST,"menuall":menuall,"content":content})
def editarticleHandler(request):
    '''
    此方法用于处理前端表单传过来的修改的文章
    :param request:
    :return:
    '''
    print("进了editarticleHandler")
    id = request.POST.get("id")
    # print(id)
    title = request.POST.get("title")
    headImg = request.FILES.get("headimg")
    titleColor = request.POST.get("color")
    column = request.POST.get("column")
    content = request.POST.get("content")
    lasttime = datetime.now()
    # print(title,headImg,titleColor,column,content,lasttime)
    # 先判断文件是否存在  存在再判断文件是否符合标准
    # print("新上传的图片为：",headImg)
    if headImg:
        # print("传了新的图片")
        print(headImg.name.split(".")[-1])
        print(settings.UPLOAD["type"])
        if headImg.name.split(".")[1] not in settings.UPLOAD["type"]:
            # print("111")
            return JsonResponse(utils.returnResult(1, "文件类型不正确"))
        imgsize = utils.getsize(headImg.size)
        # print("=====",float(imgsize))
        if float(imgsize) > settings.UPLOAD["unit"]:
            return JsonResponse(utils.returnResult(1, "文件过大"))
        # 走到这里说明文件符合要求，可以储存了
        filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
        # print(filename)
        dir = "static/uploads"
        utils.creatDir(dir)
        savePath = dir + "/" + filename
        # print("savePath为",savePath)
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
        # 修改写入数据库
        preImg = request.POST.get("preImg")
        print("表单传过去的隐藏的缩略图图片为：", preImg)
        if preImg:
            os.remove("static/uploads/"+preImg)
        news.objects.filter(id=id).update(catid=column, title=title, title_font_color=titleColor, thumb=filename, num=0,lasttime=lasttime)
    else:
        # 没有选择图片进来
        news.objects.filter(id=id).update(catid=column, title=title, title_font_color=titleColor, num=0,
                                          lasttime=lasttime)
    news_content.objects.filter(newid=id).update(content=content)
    return JsonResponse(utils.returnResult(0, "修改文章成功"))
def detailcontent(request):
    contentid=request.GET.get("id")
    print(contentid)
    detailcontent=news_content.objects.get(newid=contentid)
    print(detailcontent)
    return render(request, "temp-server/detailcontent.html", {"detailcontent":detailcontent})
def addPosition(request):
    newsIdList=request.POST.getlist("newsAd")
    position=request.POST.get("position")
    # print(newsIdList)
    # print(position)
    for item in newsIdList:
        position_content(positionid=position,newsid=item).save()
    return JsonResponse(utils.returnResult(0, "推送文章成功"))
def repos(request):
    reposlist=position.objects.all()
    return render(request, "temp-server/repos.html",{"reposlist":reposlist})
def reposcontent(request):
    newscontentlist=position_content.objects.all()
    newslist=news.objects.all()
    for item in newscontentlist:
        newsid=item.newsid
        result1=filter(lambda x:x.id==newsid,newslist)
        newslisttemp=list(result1)
        if newslisttemp:
            item.title=newslisttemp[0].title
            item.thumb=newslisttemp[0].thumb
            item.lasttime = newslisttemp[0].lasttime
    return render(request, "temp-server/reposcontent.html",{"newscontentlist":newscontentlist})
def editrepos(request):
    positionlist=position.objects.all()
    id = request.GET.get("id")
    print(id)
    positionid=position_content.objects.values("positionid").filter(id=id).get()["positionid"]
    print(positionid)
    newsid = position_content.objects.values("newsid").filter(id=id).get()["newsid"]
    print(newsid)
    positionname=position.objects.filter(id=positionid)[0].name
    # print(positionname)
    return render(request, "temp-server/editrepos.html",{"positionlist":positionlist,"positionname":positionname,"newsid":newsid})
def editreposHandler(request):
    newpositionid=request.POST.get("position")
    print(newpositionid)           #2
    newsid = request.POST.get("newsid")
    print(newsid)       #171
    position_content.objects.filter(newsid=newsid).update(positionid=newpositionid)
    return  JsonResponse(utils.returnResult(0,"修改成功"))
def deleterepos(request):
    '''
    删除推荐位的方法
    :param request:
    :return:
    '''
    reposid = request.GET.get("reposid")
    try:
        position_content.objects.filter(id=reposid).delete()
        return JsonResponse(utils.returnResult(0, "删除成功"))
    except Exception as e:
        return JsonResponse(utils.returnResult(1, "删除失败"))
def user(request):
    content = admin.objects.values("id","username","email","lasttime","heading","briefInfo").all()
    # namelist={
    #     "nameList":content
    # }
    print(content)
    return render(request, "temp-server/user.html",{"nameList":content})
def userHandler(request):
    username = request.POST.get('name')
    pwd = request.POST.get('pwd')
    email=request.POST.get('email')
    briefInfo = request.POST.get('content')
    lasttime=datetime.now()
    headImg = request.FILES.get("heading")
    list = admin.objects.values("username").all()
    for item in list:
        print(item["username"])
        if item["username"]==username:
            return JsonResponse(utils.returnResult(1, "用户已经存在"))
    size=headImg.size
    if float(size) > 10:
        print("文件过大")
    if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        print("文件类型不正确")
    filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
    savePath = "static/uploads/" + filename
    # 写入文件中
    with open(savePath, 'wb') as f:
        for file in headImg.chunks():
            f.write(file)
            f.flush()
    # print(username,pwd,email,lasttime,filename)
    newuser = admin(username=username,password=pwd,email=email,lasttime=lasttime,heading=filename,briefInfo=briefInfo)
    newuser.save()
    return JsonResponse(utils.returnResult(0, "增加用户名成功"))
class TestUEditorForm(forms.Form):
    content = UEditorField('', width=600, height=300, toolbars="full", imagePath="static/images/", filePath="static/files/",
    upload_settings={"imageMaxSize":1204000},
    settings={})
def adduser(request):
    form=TestUEditorForm()
    return render(request,"temp-server/adduser.html",{"form":form})
def adduseredit(request):
    userid = request.GET.get("userid")
    print("进了adduseredit",userid)
    nowuser = admin.objects.values("username", "password","email","heading","briefInfo").get(id=userid)
    print(nowuser)
    return JsonResponse(utils.returnResult(0,"",nowuser))
    # print("接收到前段传过来的id为",idvalue)
def edituser(request):
    form = TestUEditorForm()
    id=request.GET.get("id")
    # print(id)
    userinfo=admin.objects.values("id","username","password","email","briefInfo","heading").filter(id=id)
    # print(userinfo)
    for item in userinfo:
        userInfo=item
    return render(request, "temp-server/edituser.html",{"form":form,"userInfo":userInfo})
def edituserHandler(request):
    # print("进了edituserHandler")
    hiddenid = request.POST.get('hiddenid')
    print("当前hiddenid为",hiddenid)
    username = request.POST.get('name')
    pwd = request.POST.get('pwd')
    email = request.POST.get('email')
    briefInfo = request.POST.get('content')
    lasttime = datetime.now()
    headImg = request.FILES.get("headimg")
    # print(headImg)
    if headImg:
        # print(headImg.name.split(".")[-1])
        if headImg.name.split(".")[1] not in settings.UPLOAD["type"]:
            # print("111")
            return JsonResponse(utils.returnResult(1, "文件类型不正确"))
        imgsize = utils.getsize(headImg.size)
        # print("=====",float(imgsize))
        if float(imgsize) > settings.UPLOAD["unit"]:
            return JsonResponse(utils.returnResult(1, "文件过大"))
        filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
        dir = "static/uploads"
        utils.creatDir(dir)
        savePath = dir + "/" + filename
        # print("savePath为",savePath)
        # 写入文件中
        with open(savePath, 'wb') as f:
            for file in headImg.chunks():
                f.write(file)
                f.flush()
        # 修改写入数据库
        preImg = request.POST.get("preImg")
        print("表单传过去的隐藏的缩略图图片为：", preImg)
        os.remove("static/uploads/" + preImg)
        admin.objects.filter(id=hiddenid).update(username=username, password=pwd, email=email, lasttime=lasttime,heading=filename, briefInfo=briefInfo)
    else:
        # 没有选择图片进来
        admin.objects.filter(id=hiddenid).update(username=username,password=pwd,email=email,lasttime=lasttime,briefInfo=briefInfo)
    return JsonResponse(utils.returnResult(0, "更改用户信息成功"))
def deleteuser(request):
    idvalue = request.GET.get("idvalue")
    admin.objects.filter(id=idvalue).delete()
    return JsonResponse(utils.returnResult(0, "删除成功"))
def clear(request):
    # 清理富文本编辑器里的无用图片
    # print("8989")
    imagesimg = os.listdir(os.path.join(os.getcwd(), "static/images"))
    print(imagesimg)
    content = news_content.objects.all()
    newcontentlist = []
    for item in content:
        content = item.content
        pattern = '<img.*?src="/static/images/(.*?)".*?/>'
        m = re.findall(pattern, content)
        if m:
            newcontentlist.extend(m)
    diffimages = list(filter(lambda x: x not in newcontentlist, imagesimg))
    print(diffimages)
    if len(diffimages) != 0:
        for item in diffimages:
            os.remove("static/images/" + item)
    return render(request, "temp-server/clear.html")

