from django.db import models
from authapp.models import HabrUser
from ckeditor.fields import RichTextField


class News(models.Model):
    DRAFT = 'DF'
    PUBLISHED = 'PB'
    DELETED = 'DT'
    STATUSES = (
        (DRAFT, 'Черновик'),
        (PUBLISHED, 'Опубликованно'),
        (DELETED, 'Удалено'),
    )
    author = models.ForeignKey(HabrUser, on_delete=models.DO_NOTHING,
                               verbose_name="Автор")
    title = models.CharField(verbose_name="Название", max_length=100)
    anons = models.CharField(verbose_name="Анонс", max_length=250)
    full_text = RichTextField(verbose_name='Текст новости', blank=True, null=True)
    date = models.DateTimeField(verbose_name="Дата публикации", auto_now=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновленна')
    status = models.CharField(verbose_name="Статус новости", choices=STATUSES, max_length=128, default='DF')
    image = models.ImageField(verbose_name='Новостное изображение',
                              upload_to='media/news_photos/', blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def delete(self, using=None, keep_parents=False):
        self.status = 'DT' if self.status != 'DT' else 'DF'
        self.save()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
