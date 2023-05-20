from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginaction,name='login'),
    path('user/',views.loggedin,name='user'),
    path('destination/',views.dest,name='destiantion'),
    path('userProfile/',views.profile,name='userProfile'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("packages", views.packages, name='packages'),
    path("packages/<str:pkid>", views.packageDetails, name='packageDetails'),
]
