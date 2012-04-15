from django.contrib.auth.models import User
from django.test import TestCase

from django_twilio.models import Caller


class CallerAdminTest(TestCase):

    def setUp(self):
        # Create a superuser for testing the admin panel:
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.is_staff = True
        user.is_superuser = True
        user.save()

        # Create a test client which is already logged in as a superuser:
        self.client.login(username='test', password='test')

    def test_page_loads(self):
        response = self.client.get('/admin/django_twilio/caller/')
        self.assertEqual(response.status_code, 200)

    def test_page_lists_callers(self):
        c1 = Caller.objects.create(phone_number='+18182223333')
        c2 = Caller.objects.create(phone_number='+18183334444')

        response = self.client.get('/admin/django_twilio/caller/')

        # Get the index of each caller in the HTML response:
        pos_c1 = response.content.find(c1.__unicode__())
        pos_c2 = response.content.find(c2.__unicode__())

        # Make sure that each caller was found in the HTML response:
        self.assertNotEqual(pos_c1, -1)
        self.assertNotEqual(pos_c2, -1)

    def test_page_orders_callers_by_unicode(self):
        c1 = Caller.objects.create(phone_number='+18182179229')
        c2 = Caller.objects.create(phone_number='+18188364433')

        response = self.client.get('/admin/django_twilio/caller/')

        # Get the index of each caller in the HTML response:
        pos_c1 = response.content.find(c1.__unicode__())
        pos_c2 = response.content.find(c2.__unicode__())

        # Make sure the callers are sorted by their name:
        self.assertLess(pos_c1, pos_c2)

    def test_page_orders_callers_by_unicode_then_blacklist(self):
        c1 = Caller.objects.create(phone_number='+18002223331', blacklisted=False)
        c2 = Caller.objects.create(phone_number='+18002223333', blacklisted=True)

        response = self.client.get('/admin/django_twilio/caller/')

        # Get the index of each caller in the HTML response:
        pos_c1 = response.content.find(c1.__unicode__())
        pos_c2 = response.content.find(c2.__unicode__())

        # Make sure the callers are sorted by their name:
        self.assertLess(pos_c1, pos_c2)

    def tearDown(self):
        Caller.objects.all().delete()
        User.objects.all().delete()
        del self.client
