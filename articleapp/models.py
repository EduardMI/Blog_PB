from uuid import uuid4
from django.db import models
from django.urls import reverse
from authapp.models import HabrUser
from ckeditor.fields import RichTextField
from commentapp.middleware import get_current_user


class FilterArticle(models.Manager):
    """
    класс - Фильтр статей
    """
    def get_queryset(self):
        """
        :return:
        """
        user = get_current_user()
        if user is not None and not user.is_authenticated:
            return super().get_queryset().filter(approve=True)
        elif user is not None and user.is_staff:
            return super().get_queryset().filter(
                models.Q(approve=True) |
                models.Q(approve=False))
        return super().get_queryset().filter(
            models.Q(approve=True,
                     author=get_current_user()) |
            models.Q(approve=True))


class Category(models.Model):
    """
    класс - Категории
    """
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        """
        класс - Мета
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def delete(self, using=None, keep_parents=False):
        """
        :param using:
        :param keep_parents:
        :return:
        """
        self.is_active = False if self.is_active else True
        self.save()


class Article(models.Model):
    """
    класс - Статьи
    """
    DRAFT = 'DF'
    PUBLISHED = 'PB'
    DELETED = 'DT'
    STATUSES = (
        (DRAFT, 'черновик'),
        (PUBLISHED, 'опубликованный'),
        (DELETED, 'удалённый'),
    )
    uid = models.UUIDField(verbose_name='Ид', primary_key=True, default=uuid4)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = RichTextField(verbose_name='Текст', blank=True, null=True)
    author = models.ForeignKey(HabrUser, on_delete=models.DO_NOTHING,
                               verbose_name="Автор")
    category = models.ForeignKey(Category, blank=True, null=True,
                                 on_delete=models.DO_NOTHING,
                                 verbose_name="Категория")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    image = models.ImageField(upload_to='article_photos/', blank=True,
                              null=True, verbose_name='Изображение')
    status = models.CharField(choices=STATUSES, max_length=128, default='DF')
    liked = models.ManyToManyField(HabrUser, blank=True, related_name='likes')
    approve = models.BooleanField('Модерация', default=False)
    publication_date = models.DateTimeField(verbose_name='Дата публикации',
                                            blank=True, null=True)
    # objects = FilterArticle()

    def __str__(self):
        """
        :return:
        """
        return self.title

    class Meta:
        """
        класс - Мета
        """
        ordering = ('-created',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def get_absolute_url(self):
        """
        :return:
        """
        return reverse('article:detail', args=[self.uid])

    def delete(self, using=None, keep_parents=False):
        """
        :param using:
        :param keep_parents:
        :return:
        """
        self.status = 'DT' if self.status != 'DT' else 'DF'
        self.approve = False

        self.save()

    @property
    def num_likes(self):
        """
        :return:
        """
        return self.liked.all().count()


class Like(models.Model):

    LIKE = 'Like'
    DISLIKE = 'Like'

    LIKE_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    )

    """
    класс - Лайки
    """
    user = models.ForeignKey(HabrUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default=LIKE,
                             max_length=8)

    def __str__(self):
        """
        :return:
        """
        return str(self.article)
