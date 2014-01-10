from django.views.generic import FormView
from times.forms import TimeEntryForm


class TimeEntryAddView(FormView):
    form_class = TimeEntryForm

    def get_form_kwargs(self):
        kwargs = super(TimeEntryAddView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
