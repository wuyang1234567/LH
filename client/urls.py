from django.urls import path
from . import views

urlpatterns = [
    path("",views.main),
    path("list",views.list),
    path("detail",views.detail),
]
