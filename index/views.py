from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from server.models import *
from moudles import getdata
from django.forms import forms
from DjangoUeditor.forms import  UEditorField
from  datetime import datetime
from common import utils
from django.shortcuts import redirect
import json
from django.core.paginator import Paginator
from cms import settings
import math
import os
import re
from clearmoudles import clear
def index(request):
    # 得到当前的页码
    page = request.GET.get("page")
    if page:
        page = int(request.GET.get("page"))
    else:
        page=1
    # 得到公共的部分
    commen=getcommen()
    totalcount = news.objects.all().count()
    # 每页显示的条数
    pagecount = 4
    # 每页显示的首条id值
    pageindex = (int(page) - 1) * pagecount
    pageend=int(pageindex)+pagecount
    pages = math.ceil(totalcount / pagecount)
    # 得到所有文章的标题，时间，阅读量,图片以及文章内容
    newsallvalue = news.objects.values("title", "num","lasttime","thumb","id").order_by("-id")[int(pageindex):pageend]
    for item in newsallvalue:
        newscontent=news_content.objects.filter(newid=item["id"]).values("content")
        item["content"]=newscontent[0]["content"]
    # 分页
    num = getdata.paging(page, pages)
    everypagecountlist = range(num["startnum"], num["endnum"])
    context={
        "newsvaluelist": commen["newsvaluelist"],
        "littlenewslist": commen["littlenewslist"],
        "rightnewslist": commen["rightnewslist"],
        "newsall": commen["newsall"],
        "newsallvalue":newsallvalue,
        "pageall":pages,
        "everypagecountlist":everypagecountlist,
        "page":page,
        "menulist":commen["menulist"]
    }
    print(context["menulist"])
    return render(request, "temp-index/main.html",context)
def detail(request):
    articleid = request.GET.get("id")
    title = news.objects.values("title").get(id=articleid)
    readnum = news.objects.values("num").get(id=articleid)
    nownum = readnum["num"] + 1
    news.objects.filter(id=articleid).update(num=nownum)
    detail = news_content.objects.values("content").get(newid=articleid)
    commen=getcommen()
    context = {
        "title": title,
        "detail": detail,
        "newsvaluelist": commen["newsvaluelist"],
        "littlenewslist": commen["littlenewslist"],
        "rightnewslist": commen["rightnewslist"],
        "newsall": commen["newsall"],
        "menulist":commen["menulist"]
    }
    return render(request, "temp-index/detail.html",context)
def list(request):
    menuid= request.GET.get("id")
    menuall = menu.objects.values("name", "id").all()
    # 得到所有文章的标题，时间，阅读量,图片以及文章内容
    newsallvalue = news.objects.filter(catid=menuid).values("title", "num", "lasttime", "thumb", "id").order_by("-id")
    for item in newsallvalue:
        newscontent = news_content.objects.filter(newid=item["id"]).values("content")
        item["content"] = newscontent[0]["content"]
    print(newsallvalue)
    commen = getcommen()
    content = {
        "newsvaluelist": commen["newsvaluelist"],
        "littlenewslist": commen["littlenewslist"],
        "rightnewslist": commen["rightnewslist"],
        "newsall": commen["newsall"],
        "menulist": commen["menulist"],
        "newsallvalue":newsallvalue
    }
    return render(request, "temp-index/list.html", content)
def getcommen():
    '''
    得到公共的部分
    :return:
    '''
    positionContent = position_content.objects.values("positionid", "newsid").all()
    newsvaluelist = []
    for item in positionContent:
        # 得到轮播大图
        newsid = position_content.objects.filter(positionid=1).values("newsid").all().order_by("-id")[0:3]
    for item in newsid:
        newsvalue = news.objects.filter(id=item["newsid"]).values("title", "thumb").order_by("-id")
        newsvaluelist.extend(newsvalue)
        # 得到小广告
        littenewsid = position_content.objects.filter(positionid=2).values("newsid").all().order_by("-id")[0:3]
    littlenewslist = []
    for item in littenewsid:
        littlenewsvalue = news.objects.filter(id=item["newsid"]).values("title", "thumb").order_by("-id")
        littlenewslist.extend(littlenewsvalue)
        # 得到右侧广告
        rightnewsid = position_content.objects.filter(positionid=3).values("newsid").all().order_by("-id")[0:3]
    rightnewslist = []
    for item in rightnewsid:
        rightnewsvalue = news.objects.filter(id=item["newsid"]).values("title", "thumb").order_by("-id")
        rightnewslist.extend(rightnewsvalue)
    # 得到文章推荐
    newsall = news.objects.values("title", "num")[0:5]
    # 得到全部栏目
    menulist = menu.objects.values("name","id").all()

    return{
        "newsvaluelist":newsvaluelist,
        "littlenewslist":littlenewslist,
        "rightnewslist":rightnewslist,
        "newsall":newsall,
        "menulist":menulist
    }