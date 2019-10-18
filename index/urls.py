from django.urls import path
from . import views
urlpatterns = [
    path("",views.index),
    path("detail",views.detail),
    path("list",views.list)
]