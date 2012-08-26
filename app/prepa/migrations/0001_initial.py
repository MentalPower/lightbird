# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Town'
        db.create_table('prepa_town', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True)),
            ('add_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('prepa', ['Town'])

        # Adding model 'Area'
        db.create_table('prepa_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Town'], on_delete=models.PROTECT)),
            ('add_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('prepa', ['Area'])

        # Adding model 'Event'
        db.create_table('prepa_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Area'], on_delete=models.PROTECT)),
            ('add_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('prepa', ['Event'])

        # Adding model 'Status'
        db.create_table('prepa_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name_en', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('add_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('prepa', ['Status'])

        # Adding model 'Action'
        db.create_table('prepa_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Event'], on_delete=models.PROTECT)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Status'], on_delete=models.PROTECT)),
            ('add_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('prepa', ['Action'])


    def backwards(self, orm):
        # Deleting model 'Town'
        db.delete_table('prepa_town')

        # Deleting model 'Area'
        db.delete_table('prepa_area')

        # Deleting model 'Event'
        db.delete_table('prepa_event')

        # Deleting model 'Status'
        db.delete_table('prepa_status')

        # Deleting model 'Action'
        db.delete_table('prepa_action')


    models = {
        'prepa.action': {
            'Meta': {'object_name': 'Action'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Event']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Status']", 'on_delete': 'models.PROTECT'})
        },
        'prepa.area': {
            'Meta': {'object_name': 'Area'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Town']", 'on_delete': 'models.PROTECT'})
        },
        'prepa.event': {
            'Meta': {'object_name': 'Event'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Area']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'prepa.status': {
            'Meta': {'object_name': 'Status'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_en': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'prepa.town': {
            'Meta': {'object_name': 'Town'},
            'add_date': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'})
        }
    }

    complete_apps = ['prepa']