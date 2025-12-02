from django.contrib import admin
from .models import Document, Query


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'short_content', 'tags')
    search_fields = ('title', 'content', 'tags')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def short_content(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    short_content.short_description = "short content"

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'has_answer')
    search_fields = ('question', 'answer')
    list_filter = ('created_at')
    ordering = ('-created_at')
    readonly_fields = ('created_at')

    @admin.display(boolean=True, description="has answer?")
    def has_answer(self, obj):
        return bool(obj.answer)