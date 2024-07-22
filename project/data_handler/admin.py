from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import DataRecord


@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'encrypted_data')
    search_fields = ('name', 'encrypted_data')
    list_filter = ('name',)