from django.db import models

from articleapp.models import Article
from authapp.models import HabrUser


class ArticleRating(models.Model):
    """ Рейтинг статьи """

    class Meta:
        verbose_name = "рейтинг статьи"
        verbose_name_plural = "рейтинги статей"

    article = models.OneToOneField(Article, verbose_name='статья', primary_key=True, on_delete=models.DO_NOTHING)
    likes = models.PositiveIntegerField(verbose_name='количество лайков', default=0)
    comments = models.PositiveIntegerField(verbose_name='количество комментарий', default=0)

    def value(self):
        """ рейтинг """
        return self.likes + self.comments

    @property
    def rating(self):
        return self.value()


class AuthorRating(models.Model):
    """ Рейтинг автора """

    class Meta:
        verbose_name = "рейтинг пользователя"
        verbose_name_plural = "рейтинги пользователей"

    author = models.OneToOneField(HabrUser, verbose_name='статья', primary_key=True, on_delete=models.DO_NOTHING)
    likes = models.PositiveIntegerField(verbose_name='количество лайков', default=0)
    comments = models.PositiveIntegerField(verbose_name='количество комментарий', default=0)

    def value(self):
        """ рейтинг """
        return self.likes + self.comments

