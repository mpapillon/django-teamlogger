from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from nouvelles.models import Article, Tag, Attachment, Profile
from nouvelles.settings import SITE_NAME

admin.site.site_header = "%s / Administration" % SITE_NAME
admin.site.site_title = "%s site admin" % SITE_NAME
admin.site.unregister(User)  # Re-register UserAdmin


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 1


@admin.register(Article)
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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
