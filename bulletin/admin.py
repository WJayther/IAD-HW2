from django.contrib import admin

# Register your models here.

from bulletin.models import Bullet

class BulletAdmin(admin.ModelAdmin):
    list_display = ('name','description','datetime')
    list_filter = ['datetime']
    search_fields = ('id','name')

admin.site.register(Bullet, BulletAdmin)
