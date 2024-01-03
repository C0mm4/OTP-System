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
from django.urls import path
from .views import *

app_name = 'pybo'

urlpatterns = [
    path('', index, name = 'index'),
    path('<int:question_id>/', detail, name = 'detail'),
    path('answer/create/<int:question_id>/', answer_create, name = 'answer_create'),
    path('question/create/', question_create, name = 'question_create'),
    
]
