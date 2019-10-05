from django.shortcuts import render
import pymysql
from django.http import HttpResponse
from django.shortcuts import render,redirect
from server.models import *
import json
def main(request):
    '''
    这个方法用于从后端获取导航条的分类  例如军事，娱乐，教育等等
    :param request:
    :return:
    '''
    print("888")
    list=menu.objects.values("name").all()
    print(list)
    articlelist = news.objects.values("title","num","lasttime","id").all()
    print(articlelist)
    contentlist = news_content.objects.values("content").all()
    print(contentlist)
    content={
        'list': list,
        "articlelist": articlelist,
    }
    print(content)
    return  render(request, "temp-client/main.html",content)
def allList(request):
    '''
    这个方法用于获取首页的列表，也就是轮播图下方显示全部分类下的列表
    :param request:
    :return:
    '''
    articlelist = news.objects.values("title").all()
    # for item in articlelist:
    #     print(item["title"])
    return render(request, "temp-client/main.html",{"articlelist":articlelist})
def list(request):
    list = menu.objects.values("name").all()
    return render(request, "temp-client/list.html",{'list': list})
def detail(request):
    list = menu.objects.values("name").all()
    return render(request, "temp-client/detail.html",{'list': list})

