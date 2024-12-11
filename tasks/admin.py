from django.contrib import admin

# Register your models here.
from .models import Task

@admin.register(Task)
class TaskRegister(admin.ModelAdmin):
    list_display=("id","title")