import factory

from . import models
from times.factories import UserFactory, ActionTypeFactory


class TimeTargetFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.TimeTarget

    user = factory.SubFactory(UserFactory)
    period = 10
    target_action = factory.SubFactory(ActionTypeFactory)
    time_bound = 300
    boundary_type = 'gt'
    description = 'test target'
