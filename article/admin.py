from django.contrib import admin
from .models import Article


# Register your models here.
class ArticleManager(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'created_time', 'updated_time']
    list_display_links = ['title']
    search_fields = ['title', 'id']


admin.site.register(Article, ArticleManager)
