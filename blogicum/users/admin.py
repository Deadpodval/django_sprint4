from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from blogicum.users.models import BlogUser

admin.site.register(BlogUser, UserAdmin)
