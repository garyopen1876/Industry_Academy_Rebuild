from django.contrib import admin
from .models import Student, Resume, InterShip


class StudentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Student._meta.fields]
    search_fields = [field.name for field in Student._meta.fields]


class ResumeAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_company', 'resume']
    filter_horizontal = ['company', ]


class InterShipAdmin(admin.ModelAdmin):
    list_display = [field.name for field in InterShip._meta.fields]
    search_fields = [field.name for field in InterShip._meta.fields]


admin.site.register(Student, StudentAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(InterShip, InterShipAdmin)

