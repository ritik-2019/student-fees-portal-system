"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from myapp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome),
    path('login/', login),
    path('logout/', logout),
    path('auth_error/', auth_error),
    path('admin_reg/', admin_reg),
    path('admin_home/',admin_home),
    path('admin_edit/', admin_edit),
    path('admin_changepass/', admin_changepass),
    path('admin_prof/', admin_prof),
    path('admin_emplist/', admin_emplist),
    path('admin_stud_show/', admin_stud_show),
    path('admin_stud_edit/',admin_stud_edit),
    path('emp_del/', emp_del),
    path('emp_reg/',emp_reg),
    path('emp_changepass/', emp_changepass),
    path('emp_home/', emp_home),
    path('emp_edit/', emp_edit),
    path('emp_stud_fee/', emp_stud_fee),
    path('stud_reg/', stud_reg),
    path('stud_show/', stud_show),
    path('admin_stud_del/', admin_stud_del),
    path('emp_stud_update/', emp_stud_update),
    path('uploadphoto/', uploadphoto),
    path('emp_show_fee/', emp_show_fee),
    path('admin_show_fee/', admin_show_fee),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
