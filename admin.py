from django.contrib import admin

from nouvelles.settings import SITE_NAME
from nouvelles.models import Article, Tag, Attachment


admin.site.site_header = "%s / Administration" % SITE_NAME
admin.site.site_title = "%s site admin" % SITE_NAME


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
