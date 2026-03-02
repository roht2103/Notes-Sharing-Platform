from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Category, Note, Comment, Download


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""
    list_display = ['category_id', 'category_name', 'description', 'created_at']
    list_display_links = ['category_id', 'category_name']
    search_fields = ['category_name', 'description']
    list_per_page = 20
    ordering = ['category_name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin interface for Note model"""
    list_display = [
        'note_id',
        'title',
        'user',
        'category',
        'uploaded_date',
        'get_download_count'
    ]
    list_display_links = ['note_id', 'title']
    list_filter = ['category', 'uploaded_date']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['uploaded_date', 'get_download_count']
    list_per_page = 20
    ordering = ['-uploaded_date']

    fieldsets = (
        ('Note Information', {
            'fields': ('title', 'description', 'file')
        }),
        ('Categorization', {
            'fields': ('category',)
        }),
        ('User & Metadata', {
            'fields': ('user', 'uploaded_date', 'get_download_count')
        }),
    )

    def get_download_count(self, obj):
        """Display download count in admin"""
        return obj.get_download_count()
    get_download_count.short_description = 'Downloads'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model"""
    list_display = [
        'comment_id',
        'user',
        'note',
        'content_preview',
        'comment_date'
    ]
    list_display_links = ['comment_id']
    list_filter = ['comment_date']
    search_fields = ['content', 'user__username', 'note__title']
    readonly_fields = ['comment_date']
    list_per_page = 20
    ordering = ['-comment_date']

    def content_preview(self, obj):
        """Show preview of comment content"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    """Admin interface for Download model"""
    list_display = [
        'download_id',
        'user',
        'note',
        'download_date'
    ]
    list_display_links = ['download_id']
    list_filter = ['download_date']
    search_fields = ['user__username', 'note__title']
    readonly_fields = ['download_date']
    list_per_page = 20
    ordering = ['-download_date']


# Customize admin site headers
admin.site.site_header = 'Digital Notes Sharing Platform Admin'
admin.site.site_title = 'Notes Admin'
admin.site.index_title = 'Welcome to Digital Notes Administration'

# Remove Groups from admin panel (not needed for this application)
admin.site.unregister(Group)
