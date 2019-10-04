from django.shortcuts import render
import pymysql
from django.http import HttpResponse
from django.shortcuts import render,redirect
from server.models import *
import json
def main(request):
        print("888")
        list=menu.objects.values("name").all()
        print(list)
        return  render(request, "temp-client/main.html",{'list': list})
def list(request):
    list = menu.objects.values("name").all()
    return render(request, "temp-client/list.html",{'list': list})
def detail(request):
    list = menu.objects.values("name").all()
    return render(request, "temp-client/detail.html",{'list': list})

