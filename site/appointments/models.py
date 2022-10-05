from django.db import models
import re
from django.core.exceptions import ValidationError
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name='название региона')
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'регион'
        verbose_name_plural = 'регионы России'


class AppointDoc(models.Model):
    file_name = models.CharField(max_length=300)
    file_path = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    text_raw = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    region = models.ForeignKey(
        Region, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'appoint_doc'
        verbose_name = 'Документ о назначении'
        verbose_name_plural = 'Документы о назначении'

    def __str__(self):
        return f'Документ {self.id}'



class Person(models.Model):
    GENDER_CHOICES = (
        ('M', u'Мужской'),
        ('F', u'Женский'),
    )

    family_name = models.CharField(max_length=128, verbose_name='фамилия')
    name = models.CharField(max_length=128, verbose_name='имя')
    patronymic = models.CharField(max_length=128, verbose_name='отчество')
    appointments = models.ManyToManyField('appointments.AppointLine', related_name='app_pers', through='appointments.PersonsNAppointments')
    

    wikipedia = models.URLField(
        max_length=255, verbose_name='Ссылка на wikipedia', blank=True, null=True)
    wikipedia_id = models.CharField(max_length=128, verbose_name='Wikipedia ID', blank=True, null=True)

    # comment = models.TextField(verbose_name=u'Комментарии редактора', blank=True, null=True)
    birth_date = models.DateField(
        null=True, blank=True,
        verbose_name="Дата рождения"
    )
    death_date = models.DateField(
        null=True, blank=True,
        verbose_name="Дата смерти"
    )

    class Meta:
        ordering = ['family_name', 'name', 'patronymic']
        verbose_name = 'должностное лицо'
        verbose_name_plural = 'должностные лица'
        indexes = [
            models.Index(fields=['family_name', 'name', 'patronymic'], name='fullname_idx'),
        ]

    def get_absolute_url(self):
        return '/person/%d/' % self.pk

    def view_link(self):
        link = '/person/%d/' % self.pk
        return link

    @classmethod
    def construct_full_name(cls, family_name, name, patronymic):
        return u'%s %s %s' % (family_name, name, patronymic)

    def get_person_full_name(self):
        return self.construct_full_name(
            self.family_name, self.name, self.patronymic)

    get_person_full_name.short_description = "Полное имя"

    def get_person_short_name(self):
        return u'%s %s. %s.' % (
            self.family_name, self.name[:1], self.patronymic[:1])

    def __str__(self):
        return "%s (%s)" % (self.get_person_full_name(), self.id)

    @classmethod
    def create_from_fullname(cls, fullname):
        name_list = [d.strip() for d in re.split(r'\s|\.', fullname.title())]
        name_list = [d for d in name_list if d.strip() != '']
        if len(name_list) < 2:
            raise ValidationError(u'Нужны хотя бы имя и фамилия (%s)' % fullname)
        elif len(name_list) > 3:
            raise ValidationError(u'В ФИО должно быть не больше трёх частей (%s)' % fullname)

        family_name = name_list[0]
        name = name_list[1]
        if len(name_list) == 3:
            patronymic = name_list[2]
        else:
            patronymic = ''

        return cls(
            family_name=family_name,
            name=name,
            patronymic=patronymic,
            comment='auto')

    @classmethod
    def find_by_fullname(cls, fullname):
        name_list = fullname.strip().split()

        if len(name_list) > 3:
            raise ValueError(u'В ФИО должно быть не больше трёх частей (%s)' % fullname)
        elif len(name_list) < 1:
            raise ValidationError(u'Нужна хотя бы фамилия (%s)' % fullname)

        qs = cls.objects.filter(family_name__istartswith=name_list[0])
        if len(name_list) > 1:
            qs = qs.filter(name__istartswith=name_list[1])
        if len(name_list) > 2:
            qs = qs.filter(patronymic__istartswith=name_list[2])

        return qs

class AppointLine(models.Model):
    """
    документ может содержать несколько абзацев о назначениях, 
    в каждом из которых своя должность и персоны 
    """

    appoint_doc = models.ForeignKey(AppointDoc, models.DO_NOTHING)
    raw_line = models.TextField(verbose_name='Строка с назначением')
    position = models.CharField(max_length=700, verbose_name='Должность')
    persons = models.ManyToManyField(
        Person, related_name='pers_appoints', through='appointments.PersonsNAppointments')

    class Meta:
        managed = True
        db_table = 'appoint_line'
        unique_together = (('appoint_doc', 'position'),)
        verbose_name = 'Строка с назначением'
        verbose_name_plural = 'Строки с назначением'

    def __str__(self) -> str:
        return f'{self.position}'


class PersonsNAppointments(models.Model):
    appoint = 'appoint'
    resign = 'resign'
    actions = ((appoint, 'назначение'), (resign, 'отставка'))

    app_line = models.ForeignKey(
        AppointLine, related_name='appointees', on_delete=models.CASCADE, verbose_name='Должность')
    person = models.ForeignKey(
        Person, related_name='persons_appoints', on_delete=models.DO_NOTHING)
    action = models.CharField(
        max_length=20, default='undefined', choices=actions, verbose_name='Событие')
    is_shown = models.BooleanField(
        verbose_name='Отображается ли на сайте', default=False)

    class Meta:
        managed = True
        db_table = 'persons_n_appointments'
        unique_together = (('action', 'person', 'app_line'),)
        verbose_name_plural = "PersonsAndAppointments"

    def save(self, *args, **kwargs) -> None:
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{str(self.app_line.position)}'


class AppointPerson(Person):
    
    class Meta:
        proxy = True
        verbose_name_plural = 'Персоны с назначениями'
        verbose_name = 'Персона с назначениями'


class SelectPersonForAppointment(AppointPerson):
    """ люди, у которых совпадают имена и назначения. предполагается их сортировка вручную """

    class Meta:
        proxy = True
        verbose_name_plural = 'Назначения-дубликаты'
        verbose_name = 'Назначение-дубликат'
