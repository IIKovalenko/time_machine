from datetime import date
import json
from urllib.parse import urlencode
from django.core.urlresolvers import reverse
from django.test import TestCase

from . import factories


class TimeEntryTestCase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.action_types = [
            factories.ActionTypeFactory(),
            factories.ActionTypeFactory(name='Project 2', color='#F7464A'),
        ]
        self.time_entries = [
            factories.TimeEntryFactory(user=self.user, action_type=self.action_types[0]),
            factories.TimeEntryFactory(user=self.user, action_type=self.action_types[1]),
        ]
        for entry in self.time_entries:
            entry.spent_on = date(2013, 1, 1)
            entry.save()

    def get_url(self, url_name, params):
        return '%s?%s' % (reverse(url_name), urlencode(params))

    def get_decoded_response(self, url_name, params):
        url = self.get_url(url_name, params)
        raw_response = self.client.get(url)
        return json.loads(raw_response.content.decode('utf-8'))


class StatisticsTestCase(TimeEntryTestCase):
    def setUp(self):
        super(StatisticsTestCase, self).setUp()
        self.client.login(username=self.user.username, password='123456')

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
