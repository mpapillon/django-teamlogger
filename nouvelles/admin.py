from django.contrib import admin

from nouvelles.settings import SITE_NAME
from teamlogger.settings import APP_CONTEXT
from nouvelles.models import Article, Tag, Attachment
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin

admin.site.site_header = "%s / Administration" % SITE_NAME
admin.site.site_title = "%s site admin" % SITE_NAME


class AdminPage(admin.sites.AdminSite):
    site_url = APP_CONTEXT
    site_header = "%s / Administration" % SITE_NAME
    site_title = "%s site admin" % SITE_NAME

    def __init__(self, *args, **kwargs):
        super(AdminPage, self).__init__(*args, **kwargs)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'criticality', 'effective_date', 'author', 'creation_date')
    list_filter = ('criticality', 'effective_date', 'author')
    search_fields = ['title', 'description']
    fieldsets = [
        (None,                {'fields': ['title']}),
        ('Article content',   {'fields': ['criticality', 'effective_date', 'author', 'description']}),
        ('Article additions', {'fields': ['parent_article', 'tags', 'attachments']}),
        ('Article edition',   {'fields': ['editor', 'edition_date']})
    ]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'content_type', 'upload_by', 'upload_date')
    list_filter = ('upload_date', 'content_type')
    search_fields = ['file_name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin_page = AdminPage(name='adminpage')
admin_page.register(Article)
admin_page.register(Attachment)
admin_page.register(Tag)
admin_page.register(Group, GroupAdmin)
admin_page.register(User, UserAdmin)
