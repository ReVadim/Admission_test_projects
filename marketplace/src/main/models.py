from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    """ Custom user model
    """
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Прошел активацию?")
    send_message = models.BooleanField(default=True, verbose_name="Слать сообщения о новых комментариях?")

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Rubric(models.Model):
    """ Class Rubric
    """
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name='Название рубрики')
    sequence_number = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок следования')
    super_rubric = models.ForeignKey(
        'SuperRubric', on_delete=models.PROTECT, null=True, blank=True, verbose_name='Надрубрика')


class RubricDataManager(models.Manager):
    """ Rubric data manager
    """
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    """ Class SuperRubric
    """
    objects = RubricDataManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('sequence_number', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubric(Rubric):
    """ Class SubRubric
    """
    objects = RubricDataManager()

    def __str__(self):
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_rubric__sequence_number', 'super_rubric__name', 'sequence_number', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'
