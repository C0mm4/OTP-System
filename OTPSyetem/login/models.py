from django.shortcuts import get_object_or_404
from django.conf import settings
from pickle import FALSE
from django.db import models
from datetime import datetime

# Create your models here.
# 시리얼 객체, 시리얼 값과 생성된 시간 (genTime) 을 가지고 있음.
class Serial(models.Model):
    serialcode = models.CharField(max_length = 16)
    genTime = models.CharField(max_length = 20, default = "2205291219")

    def __str__(self):
        return self.serialcode

# 시리얼 테이블 객체, 자신의 pk id 값과, 시리얼 객체를 ForeignKey로 참조함
class Serialtable(models.Model):
    currentSerial = models.ForeignKey('Serial', on_delete=models.CASCADE, blank = False, null = False)
    id = models.AutoField(primary_key = True)

    def __int__(self):
        return self.id

# 유저 객체, ID, 닉네임, 시리얼 테이블 id, 시리얼 등록 여부를 가지고 있음
class mUser(models.Model):
    hname = models.CharField(max_length=20)
    userID = models.CharField(max_length = 20, default = "")
    sTable = models.IntegerField(default = 0)
    isSReg = models.IntegerField(default = 1)

    def __str__(self):
        if(self.hname ==""):
            return self.userID
        else:
            return self.hname
