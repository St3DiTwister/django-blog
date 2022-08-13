from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_html_photo', 'publication_date')
    list_display_links = ('id', 'title', 'publication_date')
    search_fields = ('title', 'text')
    list_filter = ('publication_date', )

    def get_html_photo(self, object):
        if object.title_image:
            return mark_safe(f"<img src='{object.title_image.url}' width=100>")

    get_html_photo.short_description = 'Фото статьи'


admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comments_author', 'comment_text', 'article')
    list_display_links = ('id', 'comments_author', 'comment_text', 'article')


admin.site.register(Comment, CommentAdmin)