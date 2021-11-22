from django.contrib import admin
from .models import Message, Function


class FunctionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Function._meta.fields]
    search_fields = [field.name for field in Function._meta.fields]


class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.fields]
    search_fields = [field.name for field in Message._meta.fields]


admin.site.register(Function, FunctionAdmin)
admin.site.register(Message, MessageAdmin)
