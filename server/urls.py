from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("menu",views.menu),
    path("addmenu",views.addmenu),
    path("articlelist",views.articlelist),
    path("addarticle",views.addarticle),
    path("user",views.user),
    path("adduser",views.adduser),
    path("adduseredit",views.adduseredit),
    path("edituser", views.edituser),
    path("userHandler",views.userHandler),
    path("login", views.login),
    path("loginhttp", views.loginhttp),
]
