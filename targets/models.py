from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
import operator


class TimeTarget(models.Model):
    BOUNDARY_TYPES = (
        ('lt', 'less'),
        ('le', 'less or equal'),
        ('gt', 'greater'),
        ('ge', 'greater or equal'),
        ('eq', 'equal'),
    )

    user = models.ForeignKey(get_user_model())
    period = models.IntegerField(help_text='Time target period, hours')
    target_action = models.ForeignKey('times.ActionType')
    time_bound = models.IntegerField(help_text='Time bound, minutes')
    boundary_type = models.CharField(max_length=2, choices=BOUNDARY_TYPES, default='gt')
    description = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return '%s %s %s min [%s]' % (
            self.target_action,
            self.get_boundary_type_display(),
            self.time_bound,
            self.user
        )

    def calculate_status(self):
        from times.models import TimeEntry

        date_to = now()
        date_from = date_to - timedelta(hours=self.period)
        statistics = TimeEntry.get_statistics(self.user, date_from, date_to)
        time_spent = [e['absolute_value'] for a, e in statistics['actions_info'].items() if a == self.target_action.pk]
        if not time_spent:
            return False

        comparator = getattr(operator, self.boundary_type)
        return comparator(time_spent[0], self.time_bound)
