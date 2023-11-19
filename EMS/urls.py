"""
URL configuration for EMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
import employee
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from employee import urls
from employee import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('employee.urls')),
    path('employform',views.employform,name="employform"),
    path('delete_employee/<id>',views.delete_employee,name='delete_employee'),
    path('noticesend',views.noticesend,name='noticesend'),
    path('attendance',views.attendance,name='attendance'),
    path('checkattendance',views.checkattendance,name='checkattendance'),
    path('catform',views.catform,name='catform'),
    path('attendancesuccess/<new_uuid>',views.attendancesuccess,name='attendancesuccess'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        
urlpatterns += staticfiles_urlpatterns()
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)