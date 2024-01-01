from django.contrib import admin
from posts.models import Post,Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','status','publish_time']
    list_filter = ['status','author','publish_time']
    date_hierarchy = 'publish_time'
    ordering = ['status','publish_time']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','author','text','created_time','active']
    list_filter = ['post','author','created_time','active']
    search_fields = ['post','author']
    actions = ['disable','activate']

    def disable(self,queryset):
        queryset.update(active=False)

    def activate(self,queryset):
        queryset.update(active=True)
        



