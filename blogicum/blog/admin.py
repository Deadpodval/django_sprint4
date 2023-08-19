from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Location, Post, BlogUser


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "pub_date", "location"]
    search_fields = ["title", "author", "category", "pub_date", "location"]
    list_filter = ["title", "author", "category", "pub_date", "location"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


admin.site.register(BlogUser, UserAdmin)
