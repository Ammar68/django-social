from django.contrib import admin
from .models import Post, Comment, Person

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')
    search_fields = ('user', 'content')
    list_filter = ('user', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')
    search_fields = ('user', 'content')
    list_filter = ('user', )

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'is_staff']
    list_editable = ['is_active', 'is_staff']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)