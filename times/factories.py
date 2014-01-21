from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
import factory

from . import models


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = factory.Sequence(lambda a: 'dummy_user_%s' % a)
    password = factory.Sequence(lambda a: make_password('123456'))
    email = 'dummy@user.com'
    is_staff = True
    is_active = True
    is_superuser = False


class ActionTypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.ActionType

    name = 'Project 1'
    color = '#E2EAE9'
    user = factory.SubFactory(UserFactory)


class TimeEntryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.TimeEntry

    user = factory.SubFactory(UserFactory)
    action_type = factory.SubFactory(ActionTypeFactory)
    time_spend_min = 60
    spent_on = now().date()
