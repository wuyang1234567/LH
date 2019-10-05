from django.urls import path
from . import views
from django.contrib import admin
urlpatterns = [
    path("",views.main),
    # path("allList",views.allList),
    path("list",views.list),
    path("detail",views.detail),
]
