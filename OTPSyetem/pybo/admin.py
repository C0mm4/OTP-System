from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Question)

class QuestionAdmin(admin.ModelAdmin):
    search_field = ['subject']

