from targets.factories import TimeTargetFactory
from times.factories import TimeEntryFactory
from times.tests import TimeEntryTestCase


class TargetsTestCase(TimeEntryTestCase):
    def setUp(self):
        super(TargetsTestCase, self).setUp()
        self.login()

    def test_target_status_shows_up(self):
        TimeTargetFactory(user=self.user)
        response = self.get_decoded_response('targets_list')
        self.assertTrue(response)
        self.assertTrue('status' in response[0])
        self.assertFalse(response[0]['status'])

    def test_status_is_true_if_target_is_ok(self):
        TimeTargetFactory(user=self.user, target_action=self.action_types[0], time_bound=30, boundary_type='gt')
        TimeEntryFactory(user=self.user, action_type=self.action_types[0], time_spend_min=60)
        response = self.get_decoded_response('targets_list')
        self.assertTrue(response[0]['status'])
