"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.home , name='home'),
    path('loginview/', views.LoginUser, name="login"),
    path('registerview/', views.RegisterView, name="registerpage"),
    # path('login/', views.LoginUser, name="login"),
    path('add-blog/', views.add_blog, name="add_blog"),
    path('logout-view/', views.LogoutPage, name="logout"),
    path('see-blog/', views.see_blog, name="see_blog"),
    path('blog-detail/<slug>', views.blog_detail, name="blog_detail"),
    path('blog-update/<slug>/', views.blog_update, name="blog_update"),
    path('blog-delete/<id>',views.blog_delete, name="blog_delete"),
    path('xls/',views.CreateExcel, name="Excel"),
    path('upload_to_db/',views.upload_data_to_DataBase,name='UploadingToDB')
]
