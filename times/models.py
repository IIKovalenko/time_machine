from django.contrib.auth import get_user_model
from django.db import models


class TimeEntry(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='Пользователь')
    action_type = models.ForeignKey('ActionType', verbose_name='Действие')
    spent_on = models.DateField('Дата записи', auto_now_add=True)
    time_spend_seconds = models.IntegerField('Потраченное время, сек', default=0)

    def __str__(self):
        return '%s %s сек. (%s)' % (self.spent_on, self.time_spend_seconds, str(self.action_type))

    @classmethod
    def get_statistics(cls, user, date_from, date_to):
        entries = TimeEntry.objects.filter(user=user, spent_on__range=(date_from, date_to))
        actions = set([e.action_type for e in entries])
        total_time_tracked = sum([e.time_spend_seconds for e in entries])
        time_spend_per_action = {}
        for action in actions:
            time_spend_per_action[action] = sum([e.time_spend_seconds for e in entries if e.action_type == action])
        return {
            'total_time_tracked': total_time_tracked,
            'actions_info': time_spend_per_action,
        }

    class Meta:
        verbose_name = 'Запись о потраченном времени'
        verbose_name_plural = 'Записи о потраченном времени'


class ActionType(models.Model):
    name = models.CharField('Название', max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип действия'
        verbose_name_plural = 'Типы действия'
