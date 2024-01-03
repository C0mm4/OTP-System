from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *


# Create your views here.

class PostViewGenTime(viewsets.ModelViewSet):
    queryset = GetGenTime.objects.all()
    serializer_class = PostGenTime


class PostViewTryLogin(viewsets.ModelViewSet):
    queryset = OTPLogin.objects.all()
    serializer_class = PostTryLogin

