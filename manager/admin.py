from django.contrib import admin
from .models import Function


class FunctionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Function._meta.fields]
    search_fields = [field.name for field in Function._meta.fields]


admin.site.register(Function, FunctionAdmin)

