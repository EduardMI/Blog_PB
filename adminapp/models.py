from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from articleapp.models import Article
from authapp.models import HabrUser
from commentapp.models import Comments


class NotifyComment(models.Model):
    from_user = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Текст', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def delete(self, using=None, keep_parents=False):
        self.is_read = True
        self.save()

    @receiver(post_save, sender=Comments)
    def notify_comment_created(sender, instance, created, **kwargs):
        if created:
            trigger = instance.comment_text
            if trigger.startswith('@moderator'):
                notify = NotifyComment()
                notify.from_user = get_object_or_404(HabrUser, pk=instance.comment_author_id)
                notify.article = get_object_or_404(Article, uid=instance.comment_article_id)
                notify.message = trigger.replace('@moderator', '').strip()
                notify.save()
