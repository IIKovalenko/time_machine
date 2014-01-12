from django.contrib.auth import get_user_model
from django.db import models


class TimeEntry(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='Пользователь')
    action_type = models.ForeignKey('ActionType', verbose_name='Действие')
    spent_on = models.DateField('Дата записи')  # TODO auto_now_add
    time_spend_seconds = models.IntegerField('Потраченное время, сек', default=0)

    def __unicode__(self):
        return '%s %s (%s)' % (self.spent_on, self.time_spend_seconds, str(self.action_type))

    class Meta:
        verbose_name = u'Запись о потраченном времени'
        verbose_name_plural = u'Записи о потраченном времени'


class ActionType(models.Model):
    name = models.CharField('Название', max_length=1024)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип действия'
        verbose_name_plural = 'Типы действия'
