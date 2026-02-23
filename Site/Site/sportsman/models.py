from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path

class Category(models.Model):
    name_rank = models.CharField(max_length=50, db_index=True, verbose_name='Спортивный разряд')
    def __str__(self):
        return self.name_rank

    class Meta:
        verbose_name_plural = 'Спортивные разряды'
        verbose_name = 'Спортивный разряд'
        ordering = ['name_rank']


class SP(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    age = models.IntegerField(verbose_name='Возраст')
#    category = models.CharField(max_length=100, verbose_name='Разряд')
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT, verbose_name='Разряд')
    town = models.CharField(max_length=100, verbose_name='Город')
    couches = models.TextField(verbose_name='Тренерский состав')
    image_sp = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Фотография')

    def delete(self, *args, **kwargs):
        for ai in self.spimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Спортсмены'
        verbose_name = 'спортсмена'
        ordering = ['name']

class SPImage(models.Model):
    sp = models.ForeignKey(SP, on_delete=models.CASCADE, verbose_name='Спортсмен')
    image_sp = models.ImageField(upload_to=get_timestamp_path, verbose_name='Фотография')

    class Meta:
        verbose_name_plural = 'Дополнительные фотографии'
        verbose_name = 'Дополнительная фотография'

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошёл активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?')

    def delete(self, *args, **kwargs):
        for news in self.news_set.all():
            news.delete()
        super().delete(self, *args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class Rubric(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')
    super_rubric = models.ForeignKey('SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надрубрика')

class SuperRubricManager(models.Manager):
    def get_querty(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'

class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)

class SubRubric(Rubric):
    object = SubRubricManager()

    def __str__(self):
        return '%s - %s' % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'

class News(models.Model):
    rubric = models.ForeignKey(SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=40, verbose_name='Тема')
    content = models.TextField(verbose_name='Описание')
    image_news = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True,db_index=True, verbose_name='Опубликовано')

    def delete(self, *args, **kwargs):
        for ai in self.newsimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Новости'
        verbose_name = 'Новость'
        ordering = ['-created_at']

class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='Новость')
    image_news = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'






