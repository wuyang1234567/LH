from django.urls import path
from . import views
from django.contrib import admin
urlpatterns = [
    path("",views.main),
    path("list",views.list),
    path("detail",views.detail),
]
