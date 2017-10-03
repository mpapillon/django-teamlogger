from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin

from nouvelles.models import Article, Tag, Attachment, Profile
from nouvelles.settings import SITE_NAME
from teamlogger.settings import APP_CONTEXT


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 1


class AdminPage(admin.sites.AdminSite):
    site_url = APP_CONTEXT
    site_header = "%s / Administration" % SITE_NAME
    site_title = "%s site admin" % SITE_NAME

    def __init__(self, *args, **kwargs):
        super(AdminPage, self).__init__(*args, **kwargs)

admin_page = AdminPage(name='adminpage')
admin_page.register(Group, GroupAdmin)


@admin.register(Article, site=admin_page)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'criticality', 'effective_date', 'author', 'is_published')
    list_filter = ('criticality', 'effective_date', 'author')
    search_fields = ['title', 'content']
    fieldsets = [
        (None,                {'fields': ['title']}),
        ('Article content',   {'fields': ['criticality', 'effective_date', 'author', 'content']}),
        ('Article additions', {'fields': ['publication_date', 'parent_article', 'tags']}),
        ('Article edition',   {'fields': ['editor', 'edition_date']})
    ]
    inlines = [AttachmentInline]


@admin.register(Tag, site=admin_page)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(User, site=admin_page)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


