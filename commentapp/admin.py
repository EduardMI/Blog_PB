from django.contrib import admin
from .models import Comments


class CommentAdmin(admin.ModelAdmin):
    """
    класс - Комментарии в админке
    """
    list_display = (
        'comment_author',
        'comment_article',
        'comment_text',
        'comment_create',
        'comment_update',
        'comment_moderation'
    )
    list_filter = (
        'comment_moderation',
        'comment_create'
    )
    actions = ['approve_comments']
    list_per_page = 15

    def approve_comments(self, request, queryset):
        """
        :param request:
        :param queryset:
        :return:
        """
        queryset.update(comment_moderation=False)


admin.site.register(Comments, CommentAdmin)
