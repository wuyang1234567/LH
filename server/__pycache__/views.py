from django.shortcuts import render
from django.http import HttpResponse
from server.models import *
from moudles import getdata
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
from  datetime import datetime
from common import utils
from django.shortcuts import redirect
import json
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    newscount=news.objects.all()
    newsnum = news.objects.values("num").order_by("-num")
    count=newscount.count()
    name = request.session['username']
    positioncontent=position_content.objects.all()
    positioncount=positioncontent.count()
    context={
        "count":count,
        "name": name,
        "maxnum":newsnum[0]["num"],
        "positioncount":positioncount
    }
    return render(request,"temp-server/index.html",context)
def menus(request):
    menulist = menu.objects.all()
    context={
        "msg":menulist
    }
    return render(request,"temp-server/menu.html",context)
def addmenu(request):
    return render(request,"temp-server/addmenu.html")
def addmenuhttp(request):
    menutitle = request.POST.get("menutitle")
    menuall =menu.objects.all()
    for item in menuall:
        print(item.name)
        if menutitle==item.name:
            return HttpResponse(getdata.returnmsg("1", "该菜单已存在", ""))
    menucontent = menu(name=menutitle)
    menucontent.save()
    return HttpResponse(getdata.returnmsg("0","提交成功",""))
def articlelist(request):
    menuid = request.GET.get("menuid")
    currentPage=request.GET.get("page")
    print(currentPage)
    menulist=menu.objects.all()
    if menuid==None:
        newslist = news.objects.all().order_by("-lasttime")
    else:
        print(menuid)
        newslist = news.objects.filter(catid__icontains=menuid).all().order_by("-lasttime")
        print(newslist)
    li=[]
    for item in newslist:
        menuall = menu.objects.values("name").get(id=item.catid)
        obj={
            "id":item.id,
            "catid": menuall["name"],
            "thumb":"../../"+item.thumb,
            "title":item.title,
            "lasttime":item.lasttime,
            "num":item.num
            }
        li.append(obj)
    # print(li)
    # 分页
    pageinator = Paginator(li, 3)  # 设置每一页显示几条  创建一个panginator对象
    pageStus = pageinator.page(currentPage)
    # 得到推荐位的id和内容
    positionvalue=position.objects.all()
    context = {
        "stus":pageStus,
        "msg":menulist,
        "news":li,
        "positionvalue":positionvalue
    }
    return render(request,"temp-server/articlelist.html",context)
def addarticle(request):
    form = TestUEditorForm()
    # 得到所有的栏目
    menuall = menu.objects.all()
    context={
        "msg":menuall,
        "form": form,
    }
    return render(request,"temp-server/addarticle.html",context)
def user(request):
    content = admin.objects.values("id","username","email","lasttime","heading").all()
    # print(content)
    namelist={
        "nameList":content
    }
    return render(request, "temp-server/user.html",namelist)
def userHandler(request):
    username = request.POST.get('name')
    pwd = request.POST.get('pwd')
    email=request.POST.get('email')
    briefInfo = request.POST.get('briefInfo')
    lasttime=datetime.now()
    headImg = request.FILES.get("heading")
    list = admin.objects.values("username").all()
    for item in list:
        print(item["username"])
        if item["username"]==username:
            return HttpResponse(utils.returnResult(1, "用户已经存在"))
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
    newuser = admin(username=username,password=pwd,email=email,lasttime=lasttime,heading=filename)
    newuser.save()
    return HttpResponse(utils.returnResult(0, "增加用户名成功"))
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
    nowuser = admin.objects.values("username", "password","email","heading").get(id=userid)
    print(nowuser)
    return HttpResponse(utils.returnResult(0,"",nowuser))
    # print("接收到前段传过来的id为",idvalue)
def edituser(request):
    form = TestUEditorForm()
    return render(request, "temp-server/edituser.html",{"form":form})
def edituserHandler(request):
    print("进了edituserHandler")
    hiddenid = request.POST.get('hiddenid')
    # print("当前id为",hiddenid)
    username = request.POST.get('name')
    pwd = request.POST.get('pwd')
    email = request.POST.get('email')
    briefInfo = request.POST.get('briefInfo')
    lasttime = datetime.now()
    headImg = request.FILES.get("heading")
    # print(headImg)
    size = headImg.size
    if float(size) > 10:
        print("文件过大")
    if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        print("文件类型不正确")
    filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
    savePath = "static/uploads/" + filename
    # # 写入文件中
    with open(savePath, 'wb') as f:
        for file in headImg.chunks():
            f.write(file)
            f.flush()
    # print(username, pwd, email, lasttime, filename)
    admin.objects.filter(id=hiddenid).update(username=username,password=pwd,email=email,lasttime=lasttime,heading=filename)
    return HttpResponse(utils.returnResult(0, "更改用户信息成功"))
def deleteuser(request):
    idvalue = request.GET.get("idvalue")
    admin.objects.filter(id=idvalue).delete()
    return HttpResponse(utils.returnResult(0, "删除成功"))
def login(request):
    return render(request,"temp-server/login.html")
def loginhttp(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    request.session['username'] = username
    print(username,password,email)
    # time = datetime.datetime.now()
    # # 判断blog_user表是否存在此用户名
    usermsg=admin.objects.all()
    for item in usermsg:
        if item.username==username:
            userpwd=admin.objects.get(username=username)
            print(userpwd.password,password)
            if userpwd.password==password:
                return HttpResponse(getdata.returnmsg("0","登录成功",""))
            else:
                return HttpResponse(getdata.returnmsg("1","密码不正确",""))
    return HttpResponse(getdata.returnmsg("2","用户名不存在",""))
def addarticlehttp(request):
    title = request.POST.get("title")
    shortTitle = request.POST.get("shortTitle")
    headImg = request.FILES.get("headimg")
    titleColor = request.POST.get("titleColor")
    column = request.POST.get("column")
    content = request.POST.get("content")
    # 判断上传过来的文件类型是否是项目需要的：
    if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        return HttpResponse(getdata.returnmsg("1","图片格式不正确",""))
    # 创建文件名 以及指定到保存文件的路径
    filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
    savePath = "static/uploads/" + filename
    # 写入文件中
    time = datetime.now()
    # 往news表中插入数据
    newarticle = news(catid=column,title=title, title_font_color=titleColor, thumb=savePath,num="1",lasttime=time)
    newarticle.save()
    value=news.objects.all()
    # 获取刚插入的id值
    newid=value[value.count()-1].id
    # 往news_content中插入数据
    print(newid,content)
    newscontent=news_content(newid=newid,content=content)
    newscontent.save()

    with open(savePath, 'wb') as f:
        for file in headImg.chunks():
            f.write(file)
            f.flush()
    return HttpResponse(getdata.returnmsg("0","提交成功",""))
def editarticle(request):
    form = TestUEditorForm()
    newsid=request.GET.get("id")
    newsvalue=news.objects.filter(id=newsid).all()
    for item in newsvalue:
        menuall = menu.objects.values("name").get(id=item.catid)
        contentvalue =news_content.objects.values("content").get(newid=item.id)
        print(item.catid)
        obj = {
            "id": item.id,
            "catid": menuall["name"],
            "thumb": "../../" + item.thumb,
            "title": item.title,
            "lasttime": item.lasttime,
            "num": item.num,
            "content":contentvalue["content"],
            "title_font_color":color(item.title_font_color),
            "colornum":item.title_font_color,
            "catidnum":item.catid
        }
    menuall = menu.objects.all()
    context={
        "msg":obj,
        "form": form,
        "menumsg": menuall,
    }
    return render(request, "temp-server/editarticle.html",context)
def updatearticle(request):
    id= request.POST.get("id")
    # print(id)
    newsvalue = news.objects.values("thumb").get(id=id)
    # print(newsvalue['thumb'])
    title = request.POST.get("title")
    headImg = request.FILES.get("headimg")
    titleColor = request.POST.get("titleColor")
    column = request.POST.get("column")
    content = request.POST.get("content")
    print(content)
    time = datetime.now()
    if headImg==None:
        news.objects.filter(id=id).update(catid=column, title=title, title_font_color=titleColor, thumb=newsvalue['thumb'],num="0", lasttime=time)
        news_content.objects.filter(newid=id).update(content=content)
        return HttpResponse(getdata.returnmsg("0", "提交成功", ""))
    # 判断上传过来的文件类型是否是项目需要的：
    if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        return HttpResponse(getdata.returnmsg("1", "图片格式不正确", ""))
    # 创建文件名 以及指定到保存文件的路径
    filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
    savePath = "static/uploads/" + filename
    # 写入文件中

    news.objects.filter(id=id).update(catid=column, title=title, title_font_color=titleColor, thumb=savePath, num="0", lasttime=time)
    value = news.objects.all()
    news_content.objects.filter(newid=id).update(content=content)
    with open(savePath, 'wb') as f:
        for file in headImg.chunks():
            f.write(file)
            f.flush()
    return HttpResponse(getdata.returnmsg("0", "提交成功", ""))
def detailcontent(request):
    id = int(request.GET.get("id"))
    print(id)
    contentvalue = news_content.objects.values("content").get(newid=id)
    contentvalue=contentvalue["content"].split(">")[1].split("<")[0]
    print(contentvalue)
    context={
        "content":contentvalue
    }
    return render(request, "temp-server/detailcontent.html",context)
def color(color):
    # print("title_font_color",color)
    if int(color) == 0:
        return "红色"
    elif int(color) == 1:
        return "绿色"
    elif int(color) == 2:
        return "蓝色"
    else:
        return "黑色"
def deletearticle(request):
    newsid = request.GET.get("id")
    news.objects.filter(id=newsid).delete()
    news_content.objects.filter(newid=newsid).delete()
    return redirect("/server/articlelist?page=1")  # 跳转到index界面
def editmenu(request):
    id = request.GET.get("id")
    menuname=menu.objects.filter(id=id).get()
    context={
        "name":menuname
    }
    return render(request, "temp-server/editmenu.html",context)
def deletemenu(request):
    id = request.GET.get("id")
    menu.objects.filter(id=id).delete()
    return redirect("/server/menus")
def updatemenu(request):
    id = request.POST.get("id")
    print(id)
    menuname = request.POST.get("menutitle")
    menuall = menu.objects.all()
    for item in menuall:
        print(menuname,item.name)
        if menuname == item.name:
            return HttpResponse(getdata.returnmsg("1", "该菜单已存在", ""))
    print("不存在")
    menu.objects.filter(id=id).update(name=menuname)
    return HttpResponse(getdata.returnmsg("0", "提交成功", ""))
def repos(request):
    repos = position.objects.all()
    context = {
        "msg": repos
    }
    return render(request, "temp-server/repos.html",context)
def reposcontent(request):
    positioncontentall = position_content.objects.all()
    li=[]
    for item in positioncontentall:
        # print(item.id,item.newsid,item.positionid)
        positionall = position.objects.filter(id=item.positionid).values("name").all()
        # print(positionall[0])
        newsall=news.objects.filter(id=item.newsid).values("title","thumb").all()
        # print(newsall)
        obj={
            "id":item.id,
            "position":positionall[0]["name"],
            "title":newsall[0]["title"],
            "thumb":"../../"+newsall[0]["thumb"],
            "time":datetime.now(),
        }
        li.append(obj)
    context={
        "msg":li
    }
    return render(request, "temp-server/reposcontent.html",context)
def pushpostion(request):
    newsid=request.GET.get("list")
    positionid=request.GET.get("positionid")
    print(newsid,positionid)
    newsid=json.loads(newsid)
    positionall = position_content.objects.filter(positionid=positionid).values("newsid").all()
    print(positionall)
    li=[]
    for item in positionall:
        print(item)
        li.append(item["newsid"])
    print(li)
    for item in newsid:
        print(item)
        position=position_content.objects.filter(newsid=item)
        if position:
            print("含有改文章推荐",position[0].positionid)
        postioncontent=position_content(positionid=positionid,newsid=item)
        postioncontent.save()
    return HttpResponse(getdata.returnmsg("0", "推送成功", ""))
def editposition(request):
    id = request.GET.get("id")
    positionid = position_content.objects.filter(id=id).get()
    # print(positionid.positionid)
    positionvalue=position.objects.filter(id=positionid.positionid).get()
    positionvalues=position.objects.all()
    context = {
        "positionvalue": positionvalue,
        "positionvalues":positionvalues
    }
    return render(request, "temp-server/editposition.html",context)
def updateposition(request):
    id= request.POST.get("id")
    print("id",id)
    position = request.POST.get("position")
    print(position)
    position_content.objects.filter(id=id).update(positionid=position)
    return HttpResponse(getdata.returnmsg("0", "提交成功", ""))
def deleteposition(request):
    id = request.GET.get("id")
    print(id)
    position_content.objects.filter(id=id).delete()
    return redirect("/server/reposcontent")
