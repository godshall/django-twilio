A simple library for building Twilio-powered Django webapps.


## Meta

* author: Randall Degges
* email:  rdegges@gmail.com
* status: maintained, stable

[![Build Status](https://secure.travis-ci.org/rdegges/django-twilio.png?branch=develop)](http://travis-ci.org/rdegges/django-twilio)


## Purpose

Building telephony applications with Twilio is easy, but not simple.

django-twilio is my attempt at reducing some of the complexities of telephony
development with Twilio--namely, implementing common patterns, helpers, etc., so
that you can truly focus on the core application logic and leave out all the
rest.


## Documentation

The documentation is hosted at ReadTheDocs. You can check out the docs
[here](http://django-twilio.rtfd.org/ "django-twilio latest").


## Changelog

v0.3: TBD

    - Adding new global setting, ``TWILIO_API_VERSION``.
    - Updating the ``Caller`` model to provide faster general usage via a
      primary key field.
    - Adding unit tests for the ``Caller`` admin hooks.
    - Refactoring existing unit tests for clarity (getting rid of fixtures).
    - Various style updates.

v0.2: 4-9-2012

    - Adding proper support for South migrations (this makes upgrading easy in
      the future).

v0.1: 3-19-2012

    - Initial release!
