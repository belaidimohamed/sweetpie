from django.contrib import admin
from .models import Album,Song
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Album,BookAdmin)
admin.site.register(Song)