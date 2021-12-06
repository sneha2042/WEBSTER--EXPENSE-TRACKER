from django.urls import path,include
from .views import *
from home import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.homepage , name = "home"),
    path('homepage/', views.home , name = "home"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        views.activate, name='activate'),  
    path('login/',auth_views.LoginView.as_view(template_name='signin.html'),name="login"),
    path('signup/',views.signup,name="signup")
]
