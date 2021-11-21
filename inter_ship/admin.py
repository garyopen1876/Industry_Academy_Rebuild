from django.contrib import admin
from .models import MonthReport


class MonthReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MonthReport._meta.fields]
    search_fields = [field.name for field in MonthReport._meta.fields]


admin.site.register(MonthReport, MonthReportAdmin)

