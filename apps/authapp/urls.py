from django.urls import path, re_path
from . import views

urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    re_path('^$', views.login),
    path('create/', views.create),
    path('logout/', views.logout),
    path('forget/', views.ForgetPwd),
    path('userinfo/', views.userinfo),
]