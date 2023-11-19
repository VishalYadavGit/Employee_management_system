from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home),
    path('employees',views.employees),
    path('notice',views.notice),
    path('attendancesheet',views.task),
]