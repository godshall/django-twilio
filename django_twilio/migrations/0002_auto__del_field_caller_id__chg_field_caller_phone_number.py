# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Caller.id'
        db.delete_column('django_twilio_caller', 'id')


        # Changing field 'Caller.phone_number'
        db.alter_column('django_twilio_caller', 'phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True))
    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Caller.id'
        raise RuntimeError("Cannot reverse this migration. 'Caller.id' and its values cannot be restored.")

        # Changing field 'Caller.phone_number'
        db.alter_column('django_twilio_caller', 'phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True))
    models = {
        'django_twilio.caller': {
            'Meta': {'object_name': 'Caller'},
            'blacklisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        }
    }

    complete_apps = ['django_twilio']
