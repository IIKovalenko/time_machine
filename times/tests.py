from datetime import date
import json

from urllib.parse import urlencode
from django.core.urlresolvers import reverse
from django.test import TestCase

from . import factories
from times.models import TimeEntry, ActionType


class TimeEntryTestCase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.action_types = [
            factories.ActionTypeFactory(user=self.user),
            factories.ActionTypeFactory(user=self.user, name='Project 2', color='#F7464A'),
        ]
        self.time_entries = [
            factories.TimeEntryFactory(user=self.user, action_type=self.action_types[0], time_spend_min=60),
            factories.TimeEntryFactory(user=self.user, action_type=self.action_types[1], time_spend_min=60),
        ]
        for entry in self.time_entries:
            entry.spent_on = date(2013, 1, 1)
            entry.save()

    def get_url(self, url_name, params):
        return '%s?%s' % (reverse(url_name), urlencode(params))

    def get_decoded_response(self, url_name, params=None):
        params = params or {}
        url = self.get_url(url_name, params)
        raw_response = self.client.get(url)
        return self._decode_response(raw_response)

    def make_post_request(self, url_name, data):
        url = reverse(url_name)
        raw_response = self.client.post(url, data=data)
        return self._decode_response(raw_response)

    def _decode_response(self, raw_response):
        return json.loads(raw_response.content.decode('utf-8'))

    def login(self):
        self.client.login(username=self.user.username, password='123456')


class LoggedInTestCase(TimeEntryTestCase):
    def setUp(self):
        super(LoggedInTestCase, self).setUp()
        self.login()


class APITestCase(LoggedInTestCase):

    def test_shows_statistics(self):
        response = self.get_decoded_response('user_statistics_view', {
            'date_from': '2013-01-01T00:00:00',
            'date_to': '2013-01-02T00:00:00'
        })
        self.assertEqual(response, {
            str(self.action_types[0].pk): {
                'color': self.action_types[0].color,
                'absolute_value': 60,
                'relative_value': 50.0
            },
            str(self.action_types[1].pk): {
                'color': self.action_types[1].color,
                'absolute_value': 60,
                'relative_value': 50.0
            },
        })

    def test_not_fails_if_no_entries(self):
        response = self.get_decoded_response('user_statistics_view', {
            'date_from': '2014-01-01T00:00:00',
            'date_to': '2014-01-02T00:00:00'
        })
        self.assertEqual(response, {})

    def test_not_fails_if_no_dates(self):
        response = self.get_decoded_response('user_statistics_view', {})
        self.assertEqual(response, {'errors': ['Specify date_from and date_to GET params.']})

    def test_can_create_entries(self):
        spent_time = 13
        response = self.make_post_request('time_entry_list', {
            'action_type': self.action_types[0].pk,
            'time_spend_min': spent_time,
        })
        self.assertTrue('id' in response)
        new_entry = TimeEntry.objects.filter(pk=response['id'])  # TODO get_object_or_None
        self.assertTrue(new_entry)
        self.assertEqual(new_entry[0].time_spend_min, spent_time)
        self.assertEqual(new_entry[0].user, self.user)

    def test_can_create_action_type(self):
        action_type_name = 'feeding dragon'
        response = self.make_post_request('action_type_list', {
            'name': action_type_name
        })
        self.assertTrue('id' in response)
        new_type = ActionType.objects.filter(pk=response['id'])
        self.assertTrue(new_type)
        self.assertEqual(new_type[0].name, action_type_name)
        self.assertTrue(new_type[0].color)

    def test_actions_list_not_shows_other_users_actions(self):
        user2 = factories.UserFactory()
        wrong_action_type = factories.ActionTypeFactory(user=user2)
        action_types = self.get_decoded_response('action_type_list')
        self.assertFalse(wrong_action_type.pk in [t['id'] for t in action_types])

    def test_actions_list_shows_common_actions(self):
        common_action = factories.ActionTypeFactory(user=None)
        action_types = self.get_decoded_response('action_type_list')
        self.assertTrue(common_action.pk in [t['id'] for t in action_types])


class ProfileTestCase(LoggedInTestCase):
    def test_profile_has_Actions_in_context(self):
        response = self.client.get(reverse('profile'))
        self.assertTrue('actions' in response.context)
        self.assertEqual(len(response.context['actions']), ActionType.objects.all().count())
