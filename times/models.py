from django.contrib.auth import get_user_model
from django.db import models


class TimeEntry(models.Model):
    user = models.ForeignKey(get_user_model())
    action_type = models.ForeignKey('ActionType')
    spent_on = models.DateField(auto_now_add=True)
    time_spend_min = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s min. (%s)' % (self.spent_on, self.time_spend_min, str(self.action_type))

    @classmethod
    def get_statistics(cls, user, date_from, date_to):
        entries = TimeEntry.objects.filter(user=user.pk, spent_on__range=(date_from, date_to))
        actions = set([e.action_type for e in entries])
        total_time_tracked = sum([e.time_spend_min for e in entries])
        time_spend_per_action = {}
        for action in actions:
            time_spend = sum([e.time_spend_min for e in entries if e.action_type == action])
            time_spend_per_action[action.pk] = {
                'color': action.color,
                'absolute_value': time_spend,
                'relative_value': time_spend / total_time_tracked * 100
            }
        return {
            'total_time_tracked': total_time_tracked,
            'actions_info': time_spend_per_action,
        }


class ActionType(models.Model):
    name = models.CharField(max_length=1024)
    color = models.CharField(max_length=7)
    weight = models.SmallIntegerField(default=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('weight', )
