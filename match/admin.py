from django.contrib import admin
from .models import Admission, Result


class AdmissionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Admission._meta.fields]
    search_fields = [field.name for field in Admission._meta.fields]


class ResultAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Result._meta.fields]
    search_fields = [field.name for field in Result._meta.fields]


admin.site.register(Admission, AdmissionAdmin)
admin.site.register(Result, ResultAdmin)
