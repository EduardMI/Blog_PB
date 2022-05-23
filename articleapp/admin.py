from django.contrib import admin
from articleapp.models import Category, Article, Like


class ArticleAdmin(admin.ModelAdmin):
    """
    класс - Статьи в админке
    """
    list_display = (
        'author',
        'title',
        'content',
        'created',
        'updated',
        'approve'
    )
    list_filter = (
        'approve',
        'created'
    )
    actions = ['approve_article']
    list_per_page = 5

    def approve_article(self, request, queryset):
        """
        :param request:
        :param queryset:
        :return:
        """
        queryset.update(approve=True)


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Like)
