from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("login", views.login),
    path("loginHandler",views.loginHandler),
    path("quitlogin", views.quitlogin),
    path("menus",views.menus),
    path("user",views.user),
    path("adduser",views.adduser),
    path("edituser", views.edituser),
    path("deleteuser", views.deleteuser),
    path("adduseredit",views.adduseredit),
    path("edituserHandler",views.edituserHandler),
    path("userHandler",views.userHandler),
    path("addmenu",views.addmenu),
    path("addmenuHandler",views.addmenuHandler),
    path("articlelist",views.articlelist),
    path("addarticle",views.addarticle),
    path("repos",views.repos),
    path("reposcontent",views.reposcontent),
    path("editrepos",views.editrepos),
    path("editreposHandler",views.editreposHandler),
    path("deleterepos",views.deleterepos),
    path("editmenu",views.editmenu),
    path("deletemenu",views.deletemenu),
    path("editmenuHandler",views.editmenuHandler),
    path("addarticleHandler",views.addarticleHandler),
    path("editarticle",views.editarticle),
    path("editarticleHandler",views.editarticleHandler),
    path("addPosition",views.addPosition),
    path("detailcontent",views.detailcontent),
    path("clear",views.clear),
]
