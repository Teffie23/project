from django.contrib import admin
from .models import *


class userAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create', 'time_update', 'num_scaf')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'time_create')
    list_editable = ('num_scaf',)
    list_filter = ('num_scaf', 'time_create')
    prepopulated_fields = {'slug': ('name',)}


class trainerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_train')
    list_display_links = ('id', 'name_train')
    search_fields = ('name_train',)
    prepopulated_fields = {'slug': ('name_train',)}


class scafAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_blocks')
    list_display_links = ('id',)
    search_fields = ('id',)


class tarifAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_tarif', 'bye')
    list_display_links = ('id', 'name_tarif', 'bye')
    search_fields = ('id', 'name_tarif', 'bye')
    prepopulated_fields = {'slug': ('name_tarif',)}


admin.site.register(tarif, tarifAdmin)
admin.site.register(user, userAdmin)
admin.site.register(trainer, trainerAdmin)
admin.site.register(scaf, scafAdmin)
# Register your models here.
