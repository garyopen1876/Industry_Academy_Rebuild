from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Message, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'get_role', 'is_staff')
    list_select_related = ('profile',)

    def get_role(self, instance):
        if instance.profile.role == 1:
            return '學生'
        elif instance.profile.role == 2:
            return '企業-人資'
        elif instance.profile.role == 3:
            return '管理者'
        elif instance.profile.role == 4:
            return '企業-實習導師'
        elif instance.profile.role == 5:
            return '大學-實習導師'
    get_role.short_description = '身分'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class MessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Message._meta.fields]
    search_fields = [field.name for field in Message._meta.fields]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)
