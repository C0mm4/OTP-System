from rest_framework import serializers
from .models import *


class PostGenTime(serializers.ModelSerializer):
    class Meta:
        model = GetGenTime
        fields = ('uID', 'Password', 'TimeCode', )

class PostTryLogin(serializers.ModelSerializer):
    class Meta:
        model = OTPLogin
        fields = ('uID', 'Password')
        
