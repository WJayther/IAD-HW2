from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from bulletin.models import *


class BulletAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'datetime')
    list_filter = ['datetime']
    search_fields = ('id', 'name')

admin.site.register(Bullet, BulletAdmin)


class FollowInline(admin.TabularInline):
    model = MyUser.follows.through
    fk_name = 'from_myuser'


class MyUserAdmin(UserAdmin):
    inlines = (FollowInline,)
    exclude = ['follows']
    pass

admin.site.register(MyUser, MyUserAdmin)
