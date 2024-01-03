"""OTPSyetem URL Configuration

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
from django.urls import path, include, re_path
from rest_framework import routers
from pybo import views as pviews
from RestAPI import views as Rviews

router = routers.DefaultRouter()
router.register(r'sync',Rviews.PostViewGenTime)
router.register(r'certification',Rviews.PostViewTryLogin)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('login/', include('login.urls')),
    path('', pviews.index, name ='index'),
    path('rest/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),

]
