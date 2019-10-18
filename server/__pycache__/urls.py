from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("menus",views.menus),
    path("addmenu",views.addmenu),
    path("articlelist",views.articlelist),
    path("addarticle",views.addarticle),
    path("user",views.user),
    path("adduser",views.adduser),
    path("adduseredit",views.adduseredit),
    path("edituser", views.edituser),
    path("edituserHandler",views.edituserHandler),
    path("userHandler",views.userHandler),
    path("deleteuser", views.deleteuser),
    path("login", views.login),
    path("loginhttp", views.loginhttp),
    path("addarticlehttp", views.addarticlehttp),
    path("editarticle",views.editarticle),
    path("updatearticle",views.updatearticle),
    path("detailcontent",views.detailcontent),
    path("deletearticle",views.deletearticle),
    path("addmenuhttp",views.addmenuhttp),
    path("editmenu",views.editmenu),
    path("deletemenu",views.deletemenu),
    path("updatemenu",views.updatemenu),
    path("repos",views.repos),
    path("reposcontent",views.reposcontent),
    path("pushpostion",views.pushpostion),
    path("editposition",views.editposition),
    path("updateposition",views.updateposition),
    path("deleteposition",views.deleteposition)
]
