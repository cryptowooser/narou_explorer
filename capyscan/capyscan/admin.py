from django.contrib import admin
from .models import NovelInfo

@admin.register(NovelInfo)
class NovelInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'ncode', 'writer', 'biggenre', 'genre']
