from django.contrib import admin
from .models import Company, VacancyRequirement, ContactPerson


class CompanyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Company._meta.fields]
    search_fields = [field.name for field in Company._meta.fields]


class VacancyRequirementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VacancyRequirement._meta.fields]
    search_fields = [field.name for field in VacancyRequirement._meta.fields]


class ContactPersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContactPerson._meta.fields]
    search_fields = [field.name for field in ContactPerson._meta.fields]


admin.site.register(Company, CompanyAdmin)
admin.site.register(VacancyRequirement, VacancyRequirementAdmin)
admin.site.register(ContactPerson, ContactPersonAdmin)
