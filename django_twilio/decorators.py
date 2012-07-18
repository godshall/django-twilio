"""Useful decorators."""


from functools import wraps

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, HttpResponseForbidden

from twilio.twiml import Verb
from twilio.util import RequestValidator

from django_twilio import settings as django_twilio_settings
from django_twilio.exceptions import InvalidMethodError
from django_twilio.utils import get_blacklisted_response


def twilio_view(method='POST', blacklist=True):
    """This decorator provides several helpful shortcuts for writing Twilio
    views.

        - It ensures that only requests from Twilio are passed through. This
          helps protect you from forged requests.

        - It ensures your view is exempt from CSRF checks via Django's
          @csrf_exempt decorator. This is necessary for any view that accepts
          POST requests from outside the local domain (eg: Twilio's servers).

        - It enforces the blacklist. If you've got any ``Caller``s who are
          blacklisted, any requests from them will be rejected.

        - It allows your view to (optionally) return TwiML to pass back to
          Twilio's servers instead of building a ``HttpResponse`` object
          manually.

        - It allows your view to (optionally) return any ``twilio.Verb`` object
          instead of building a ``HttpResponse`` object manually.

          .. note::
            The forgery protection checks ONLY happen if ``settings.DEBUG =
            False`` (aka, your site is in production).

    Usage::

        from twilio.twiml import Response

        @twilio_view
        def my_view(request):
            r = Response()
            r.sms('Thanks for the SMS message!')
            return r
    """
    method = method.lower()

    # Ensure that the specified HTTP method is valid:
    if not any((method == 'get', method == 'post')):
        raise InvalidMethodError

    # Assign the proper method handling function:
    require_method = require_POST if method == 'post' else require_GET

    def decorator(f):
        """The actual decorator to generate."""

        @wraps(f)
        def wrapped(request, *args, **kwargs):
            """The wrapped function that our decorator will return."""

            # Using the ``method`` param, ensure the incoming HTTP request is
            # the correct type (either GET or POST):
            wrapped_func = require_method(f)

            # Only handle Twilio forgery protection stuff if:
            #
            #   - Debug is currently disabled (eg: we're in production), and
            #   - The request is a POST.
            #
            # If both of these are true, then it means we need to check the
            # crypto hash that Twilio sends us to ensure that Twilio is indeed
            # the one sending the request.
            #
            # See: http://www.twilio.com/docs/security#validating-requests
            if not settings.DEBUG and request.method == 'POST':

                # Attempt to gather all required information to allow us to check the
                # incoming HTTP request for forgery. If any of this information is not
                # available, then we'll throw a HTTP 403 error (forbidden).
                #
                # The required fields to check for forged requests are:
                #
                #   1. ``TWILIO_ACCOUNT_SID`` (set in the site's settings module).
                #   2. ``TWILIO_AUTH_TOKEN`` (set in the site's settings module).
                #   3. The full URI of the request, eg: 'http://mysite.com/test/view/'.
                #      This may not necessarily be available if this view is being
                #      called via a unit testing library, or in certain localized
                #      environments.
                #   4. A special HTTP header, ``HTTP_X_TWILIO_SIGNATURE`` which
                #      contains a hash that we'll use to check for forged requests.
                if isinstance(response, HttpResponse):
                    return response

                # Validate the request
                try:
                    validator = RequestValidator(django_twilio_settings.TWILIO_AUTH_TOKEN)
                    url = request.build_absolute_uri()
                    signature = request.META['HTTP_X_TWILIO_SIGNATURE']
                except (AttributeError, KeyError):
                    return HttpResponseForbidden()

                # Now that we have all the required information to perform forgery
                # checks, we'll actually do the forgery check.
                if not validator.validate(url, request.POST, signature):
                    return HttpResponseForbidden()

            # If the user requesting service is blacklisted, reject their
            # request.
            if blacklist:
                blacklisted_resp = get_blacklisted_response(request)
                if blacklisted_resp:
                    return blacklisted_resp


            # Run the wrapped view, and capture the data returned.
            response = wrapped_func(request, *args, **kwargs)

            # If the view returns a string (or a ``twilio.Verb`` object), we'll
            # assume it is XML TwilML data and pass it back with the appropriate
            # mimetype. We won't check the XML data because that would be too time
            # consuming for every request. Instead, we'll let the errors pass
            # through to be dealt with by the developer.
            if isinstance(response, str):
                return HttpResponse(response, mimetype='application/xml')
            elif isinstance(response, Verb):
                return HttpResponse(str(response), mimetype='application/xml')
            else:
                return response

        # If the developer wants us to force a POST from Twilio, make sure we make
        # the view exempt from CSRF checks:
        if method == 'post':
            wrapped = csrf_exempt(wrapped)

        return wrapped

    return decorator
