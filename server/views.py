from django.shortcuts import render

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