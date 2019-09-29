from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("menu",views.menu),
    path("addmenu",views.addmenu),
    path("articlelist",views.articlelist),
    path("addarticle",views.addarticle),
]
