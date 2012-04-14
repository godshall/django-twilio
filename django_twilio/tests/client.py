from django.conf import settings
from django.test import TestCase
from twilio.rest import TwilioRestClient

from django_twilio.client import twilio_client


class TwilioClientTestCase(TestCase):

    def test_exists(self):
        self.assertIsInstance(twilio_client, TwilioRestClient)

    def test_sets_creds(self):
        self.assertEqual(twilio_client.auth, (settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN))

    def test_sets_api_version_to_default(self):
        self.assertIn(settings.TWILIO_API_VERSION, twilio_client.account_uri)
