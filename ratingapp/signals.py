from django.db.models.signals import post_save, post_init, post_delete, m2m_changed
from django.dispatch import receiver

from articleapp.models import Article
from commentapp.models import Comments
from ratingapp.models import ArticleRating, AuthorRating

from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=Comments)
def post_save_comment_handler(sender, **kwargs):
    """ Добавление в статистику количество комментариев """
    article_uid = kwargs['instance'].comment_article.uid
    author = kwargs['instance'].comment_article.author
    author_id = author.id
    if kwargs['created']:

        # Увеличиваем счётчик для статьи
        try:
            rating = ArticleRating.objects.get(article__uid=article_uid)
        except ObjectDoesNotExist:
            rating = ArticleRating(article=kwargs['instance'].comment_article, comments=1)
        else:
            rating.comments += 1
        rating.save()

        # Увеличиваем счётчик для автора
        try:
            rating = AuthorRating.objects.get(author_id=author_id)
        except ObjectDoesNotExist:
            rating = AuthorRating(author=author, comments=1)
        else:
            rating.comments += 1
        rating.save()

    elif not kwargs['instance'].is_active:

        # Уменьшение счётчик для статьи
        try:
            rating = ArticleRating.objects.get(article__uid=article_uid)
        except ObjectDoesNotExist:
            pass
        else:
            rating.comments -= 1 if rating.comments > 0 else 0
            rating.save()

        # Уменьшение счётчик для автора
        try:
            rating = AuthorRating.objects.get(author__id=author_id)
        except ObjectDoesNotExist:
            pass
        else:
            rating.comments -= 1 if rating.comments > 0 else 0
            rating.save()


@receiver(m2m_changed, sender=Article.liked.through)
def post_save_like_handler(sender, **kwargs):
    """ Добавление в статистику количество лайков """

    article_uid = kwargs['instance'].uid
    author = kwargs['instance'].author
    author_id = author.id

    if kwargs['action'] == 'post_add':

        # Увеличиваем счётчик для статьи
        try:
            rating = ArticleRating.objects.get(article__uid=article_uid)
        except ObjectDoesNotExist:
            rating = ArticleRating(article=kwargs['instance'], likes=1)
        else:
            rating.likes += 1
        rating.save()

        # Увеличиваем счётчик для автора
        try:
            rating = AuthorRating.objects.get(author_id=author_id)
        except ObjectDoesNotExist:
            rating = AuthorRating(author=author, likes=1)
        else:
            rating.likes += 1
        rating.save()

    elif not kwargs['action'] == 'post_remove':
        # Уменьшение счётчик для статьи
        try:
            rating = ArticleRating.objects.get(article__uid=article_uid)
        except ObjectDoesNotExist:
            pass
        else:
            rating.likes -= 1 if rating.likes > 0 else 0
            rating.save()

        # Уменьшение счётчик для автора
        try:
            rating = AuthorRating.objects.get(author__id=author_id)
        except ObjectDoesNotExist:
            pass
        else:
            rating.likes -= 1 if rating.likes > 0 else 0
            rating.save()
