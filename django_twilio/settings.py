"""django_twilio specific settings."""


from django.conf import settings


TWILIO_ACCOUNT_SID = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
TWILIO_API_VERSION = getattr(settings, 'TWILIO_API_VERSION', '2010-04-01')
