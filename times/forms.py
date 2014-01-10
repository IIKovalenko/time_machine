from django import forms
from times.models import TimeEntry


class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['action_type', 'spent_on', 'time_spend_seconds']

    def __init__(self, *args, **kwargs):
        if 'user' not in kwargs:
            raise AttributeError('Не указан пользователь при создании TimeEntryForm')
        self.user = kwargs.pop('user')
        super(TimeEntryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(TimeEntryForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
