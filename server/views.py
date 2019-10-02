from django.shortcuts import render
from django.http import HttpResponse
from server.models import *
from moudles import getdata
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
from  datetime import datetime
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
    print("444")
    headImg = request.FILES.get("heading")
    print(headImg)
    size=headImg.size
    if float(size) > 10:
        print("文件过大")
    if headImg.name.split(".")[-1] not in ["jpg", "jpeg", "png"]:
        print("文件类型不正确")
    filename = "headImg_" + str(int(datetime.now().timestamp() * 1000000)) + "." + headImg.name.split(".")[-1]
    print(filename)
    savePath = "static/uploads/" + filename
    # 写入文件中
    with open(savePath, 'wb') as f:
        for file in headImg.chunks():
            f.write(file)
            f.flush()
    return render(request,"temp-server/user.html")
class TestUEditorForm(forms.Form):
    content = UEditorField('内容', width=600, height=300, toolbars="full", imagePath="static/images/", filePath="static/files/",
    upload_settings={"imageMaxSize":1204000},
    settings={})
def adduser(request):
    form=TestUEditorForm()
    return render(request,"temp-server/adduser.html",{"form":form})
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

