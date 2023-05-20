from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.dash,name='authenticate'),
    path('login/',views.login,name='login'),
    path('msg/',views.msg,name='msg'),
    path('dash/',views.dash,name='dashboard'),
    path('logout/',views.logout,name="logout"),
    path('addpackage/',views.addpackage,name="addpackage"),
    path("predict/",views.predict,name="predict")
]
