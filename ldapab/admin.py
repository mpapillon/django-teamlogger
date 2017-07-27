from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from ldapab.models import DirectoryInfo


class DirectoryInfoInline(admin.StackedInline):
    model = DirectoryInfo
    can_delete = False
    verbose_name_plural = 'LDAP Directory Information'


class UserAdmin(BaseUserAdmin):
    inlines = (DirectoryInfoInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
