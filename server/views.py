from django.shortcuts import render
from django.http import HttpResponse
from server.models import *
from moudles import getdata
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
from  datetime import datetime
from common import utils
import json
# Create your views here.
def index(request):
    return render(request,"temp-server/index.html")
def menu(request):
    return render(request,"temp-server/menu.html")
def addmenu(request):
    return render(request,"temp-server/addmenu.html")
def articlelist(request):
    return render(request,"temp-server/articlelist.html")
def addarticle(request):
    return render(request,"temp-server/addarticle.html")
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
    print(username,pwd,email,lasttime,filename)
    newuser = admin(username=username,password=pwd,email=email,lasttime=lasttime,heading=filename)
    newuser.save()
    return HttpResponse(utils.returnResult(0, "增加用户名成功"))
class TestUEditorForm(forms.Form):
    content = UEditorField('内容', width=600, height=300, toolbars="full", imagePath="static/images/", filePath="static/files/",
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
    # print(filename)
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
    print(username,password,email)
    # time = datetime.datetime.now()
    # # 判断blog_user表是否存在此用户名
    usermsg=admin.objects.all()
    for item in usermsg:
        if item.username==username:
            userpwd=admin.objects.get(username=username)
            if userpwd.password==password:
                print(userpwd,password)
                return HttpResponse(getdata.returnmsg("0","登录成功",""))
            else:
                return HttpResponse(getdata.returnmsg("1","密码不正确",""))
    return HttpResponse(getdata.returnmsg("2","用户名不存在",""))

