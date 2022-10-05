# coding: utf-8

from django.conf import settings
from django.db import models
from django.urls import reverse


class TrackUserMixin(models.Model):
    """
    Этот класс добавляет 4 поля, чтобы знать время добавления и добавившего пользователя
    Чтобы проводить "модерацию" новых значений в админке без всяких ужасов
    Поля пользователей разрешено оставлять пустыми "на всякий случай"
    Поля с датами пустые, чтобы навешивать на существующие таблицы
    TODO: Если это примесь, то наследоваться от Model не совсем верно
    """
    created_when = models.DateTimeField(verbose_name='дата добавления', blank=True, null=True, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='кто добавил', blank=True, null=True,
                                   related_name='%(class)s_created', on_delete=models.CASCADE)

    modified_when = models.DateTimeField(verbose_name='дата последнего изменения', blank=True, null=True,
                                         auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='кто изменил в последний раз', blank=True,
                                    null=True, related_name='%(class)s_modified', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class FederalDistrict(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    color = models.CharField(max_length=30, verbose_name='цвет для отображения на карте')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'declarations'
        verbose_name = 'федеральный округ'
        verbose_name_plural = 'федеральные округа'



class VerifyLogEntry(models.Model):
    checked_when = models.DateTimeField(verbose_name='Дата проверки', auto_now_add=True)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Кто проверил', on_delete=models.CASCADE)
    person = models.ForeignKey('declarations.Person', null=True,
                               verbose_name='Проверяемое должностное лицо', on_delete=models.CASCADE)
    section = models.ForeignKey('declarations.Section', null=True,
                                verbose_name='Проверяемая секция', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Запись проверки должностного лица или секции'
        verbose_name_plural = 'Записи проверки должностных лиц и секций'


class ImportSession(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сессия автоматического импорта'
        verbose_name_plural = 'Сессии автоматического импорта'
