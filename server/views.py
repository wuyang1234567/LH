from django.shortcuts import render
from django.http import HttpResponse
from server.models import *
from moudles import getdata
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

