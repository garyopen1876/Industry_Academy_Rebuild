from django.contrib import admin
from .models import Tutor


class TutorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tutor._meta.fields]
    search_fields = [field.name for field in Tutor._meta.fields]


admin.site.register(Tutor, TutorAdmin)
