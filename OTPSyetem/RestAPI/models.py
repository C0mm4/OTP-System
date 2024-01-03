from django.db import models

# Create your models here.

class GetGenTime(models.Model):
    uID = models.CharField(max_length = 20, default = "")
    Password = models.CharField(max_length = 20, default = "")
    TimeCode = models.CharField(max_length = 20, default = "2205291219")

    def __str__(self):
        return self.uID


class OTPLogin(models.Model):
    uID = models.CharField(max_length = 20, )
    Password = models.CharField(max_length = 20, default = "")


    def __str__(self):
        return self.uID
