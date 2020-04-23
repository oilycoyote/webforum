from django.contrib import admin
from .models import Board, Topic, Post

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'description')
    list_per_page = 20

class TopicAdmin(admin.ModelAdmin):
    list_display = ('subject', 'board', 'last_updated', 'starter')
    list_display_links = ('subject',)
    search_fields = ('subject',)
    list_filter = ('board',)
    list_per_page = 20

class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'message', 'created_by', 'created_at',)
    list_display_links = ('topic', 'message',)
    search_fields = ('message', 'created_by',)
    list_filter = ('topic',)
    list_per_page = 20

# Register your models here.

admin.site.register(Board, BoardAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)

