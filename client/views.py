from django.shortcuts import render
import pymysql
from django.http import HttpResponse
from django.shortcuts import render,redirect
from server.models import *
from common import utils
# from one.models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
def main(request):
    '''
    这个方法用于从后端获取各种信息显示在主页的各个位置
    :param request:
    :return:
    '''
    menuid = request.GET.get("menuid")
    # print("导航条的id",menuid)
    list=menu.objects.values("name","id").all()
    # print("none")
    articlelist = news.objects.values("title", "num", "lasttime", "id","thumb").all()
    contentlist = news_content.objects.values("content", "newid").all()
    # print(contentlist)
    arr = []
    for item in articlelist:
        obj = {
            "title": item["title"],
            "num": item["num"],
            "lasttime": item["lasttime"],
            "thumb": "../../static/uploads/" + item["thumb"],
        }
        temobj = obj.copy()
        for item1 in contentlist:
            if item["id"] == item1["newid"]:
                temobj.update(item1)
        arr.append(temobj)
    # print(arr)
    pagenow = request.GET.get("page")
    # print("当前页数：", pagenow)  # 1   当前是第几页
    paginator = Paginator(arr, 3)
    # print(paginator)
    pageStus = paginator.page(int(pagenow))
    # print(pageStus)
    # 从这开始是关于文章排行的
    allnum = news.objects.values("title", "num", "lasttime", "id").order_by("-num").all()[0:5]
    # print(allnum)
    allnum1 = news.objects.values("id").order_by("-num").all()[0:1]
    for item in allnum1:
        bignumid=item["id"]
        # print(bignumid)
    bignumcontent = news_content.objects.values("content", "newid").get(newid=bignumid)
    # print(bignumcontent)
    # 关于文章排行的结束
    # 关于轮播图片开始
    lunboid = position_content.objects.values("newsid").filter(positionid=1)[0:2]
    for item in lunboid:
        newsid=item["newsid"]
        lunbo = news.objects.values("id","title","thumb").filter(id=newsid).order_by("-id")
        item["title"]=lunbo[0]["title"]
        item["thumb"]=lunbo[0]["thumb"]
    # 关于轮播图片结束
    # 关于小广告开始
    smalladid = position_content.objects.values("newsid").filter(positionid=2).all()
    # print(smalladid)
    arrsmallad = []
    for item in smalladid:
        # print(item["newsid"])
        smallad = news.objects.values("id", "title", "thumb").filter(id=item["newsid"])
        obj = {
            "title": smallad[0]["title"],
            "thumb":smallad[0]["thumb"],
        }
        arrsmallad.append(obj)
    print(arrsmallad)
    # 关于小广告结束
    # 关于侧面广告开始
    slideadid = position_content.objects.values("newsid").filter(positionid=3).all()
    # print(slideadid)
    arrslidead = []
    for item in slideadid:
        # print(item["newsid"])
        slidead = news.objects.values("id", "title", "thumb").filter(id=item["newsid"])
        obj = {
            "title": slidead[0]["title"],
            "thumb":slidead[0]["thumb"],
        }
        arrslidead.append(obj)
    # print(arrslidead)
    # 关于侧面广告结束
    content = {
        'list': list,
        "pageStus": pageStus,
        "allnum":allnum,         #文章排行的阅读数量
        "bignumcontent":bignumcontent,
        "arrsmallad":arrsmallad,                 #小广告位的数组
        "arrslidead":arrslidead              #侧面广告位的数组
    }
    # print(content)
    return render(request, "temp-client/main.html", content,{"lunbo":lunbo})
def getDetailContent(request):
    '''
    用于详情页面传过来的id值并获取到对应的详情信息再ajax返回给前端
    :param request:
    :return:
    '''
    # print("888888")
    articleid = request.GET.get("articleid")
    print(articleid)
    title = news.objects.values("title").get(id=articleid)
    readnum = news.objects.values("num").get(id=articleid)
    print(readnum["num"])
    nownum=readnum["num"]+1
    news.objects.filter(id=articleid).update(num=nownum)
    detail = news_content.objects.values("content").get(newid=articleid)
    print(detail)
    content={
        "title":title,
        "detail":detail
    }
    return HttpResponse(utils.returnResult(0, "",content))
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
    print("999")
    menuid= request.GET.get("id")
    list = menu.objects.values("name", "id").all()
    print(menuid)
    articlelist = news.objects.values("title", "num", "lasttime", "id").filter(catid=menuid).all()
    contentlist = news_content.objects.values("content", "newid").all()
    arr = []
    for item in articlelist:
        temobj = item.copy()
        for item1 in contentlist:
            if item["id"] == item1["newid"]:
                temobj.update(item1)
        arr.append(temobj)
    print(arr)
    allnum = news.objects.values("title", "num", "lasttime", "id").order_by("-num").all()[0:5]
    print(allnum)
    allnum1 = news.objects.values("id").order_by("-num").all()[0:1]
    for item in allnum1:
        bignumid = item["id"]
        print(bignumid)
    bignumcontent = news_content.objects.values("content", "newid").get(newid=bignumid)
    print(bignumcontent)
    content = {
        'list': list,
        "arr": arr,
        "allnum": allnum,
        "bignumcontent": bignumcontent
    }
    return render(request, "temp-client/list.html", content)
    # return render(request, "temp-client/list.html",{'list': list})
def detail(request):
    list = menu.objects.values("name").all()
    return render(request, "temp-client/detail.html",{'list': list})

