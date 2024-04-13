"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from myfirstapp import views

from django.views.static import serve
from myproject.settings import MEDIA_ROOT
#from django.conf.urls import url
from django.urls import re_path as url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('base/',views.base,name='base'),
    path('personal/',views.personal,name='personal'),
    path('others_space/',views.others_space,name='others_space'),
    path('getid/',views.getid,name='getid'),
    path('read/',views.read,name='read'),
    path('login/',views.login,name='login'),
    path('getlogin/',views.getlogin,name='getlogin'),
    path('hot/',views.hot,name='hot'),
    path('follow/',views.follow,name='follow'),
    path('getusername/',views.getusername,name='getusername'),
    path('test/',views.test,name='test'),
    path('test2/',views.test2,name='test2'),
    path('get_photo/',views.get_photo,name='get_photo'),
    path('article/',views.article,name='article'),
    path('write/',views.write,name='write'),
    path('register/',views.register,name='register'),
    path('ajax',views.ajax),
    path('ajax2/',views.ajax2),
    path('modify_user/',views.modify_user),
    path('getmost_read/',views.getmost_read),
    path('get_tag/',views.get_tag),
    path('attend/',views.attend),
    #实现推流
    path('tuiliu/', include("tuiliu.urls")),
    re_path('media/(?P<path>.*)',serve,{"document_root":MEDIA_ROOT})

]
