from django.contrib import admin
from .models import Post, Comment


# customizing the admin site
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # list_display will show the fields you want displayed on the post list page
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    # list filter creates a right sidebar on admin that allows filtering of results based on what is included in the
    # list_filter attribute/variable
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    # the slug is filled as you are typing the title
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    # creates navigation links to navigate through a date hierachy
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

# customizing Comment's admin interface too
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

# Register your models here.
