# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Scan'
        db.create_table('prepa_scan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_towns', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('num_breakdowns', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('record_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('prepa', ['Scan'])

        # Adding model 'Town'
        db.create_table('prepa_town', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('scan_added', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Scan'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal('prepa', ['Town'])

        # Adding model 'Area'
        db.create_table('prepa_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Town'], on_delete=models.PROTECT)),
            ('scan_added', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Scan'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal('prepa', ['Area'])

        # Adding model 'Status'
        db.create_table('prepa_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('scan_added', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Scan'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal('prepa', ['Status'])

        # Adding model 'Event'
        db.create_table('prepa_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Area'], on_delete=models.PROTECT)),
            ('scan_added', self.gf('django.db.models.fields.related.ForeignKey')(related_name='added', on_delete=models.PROTECT, to=orm['prepa.Scan'])),
            ('scan_last_seen', self.gf('django.db.models.fields.related.ForeignKey')(related_name='last_seen', on_delete=models.PROTECT, to=orm['prepa.Scan'])),
        ))
        db.send_create_signal('prepa', ['Event'])

        # Adding model 'Action'
        db.create_table('prepa_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Event'], on_delete=models.PROTECT)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Status'], on_delete=models.PROTECT)),
            ('scan_added', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['prepa.Scan'], on_delete=models.PROTECT)),
        ))
        db.send_create_signal('prepa', ['Action'])


    def backwards(self, orm):
        # Deleting model 'Scan'
        db.delete_table('prepa_scan')

        # Deleting model 'Town'
        db.delete_table('prepa_town')

        # Deleting model 'Area'
        db.delete_table('prepa_area')

        # Deleting model 'Status'
        db.delete_table('prepa_status')

        # Deleting model 'Event'
        db.delete_table('prepa_event')

        # Deleting model 'Action'
        db.delete_table('prepa_action')


    models = {
        'prepa.action': {
            'Meta': {'object_name': 'Action'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Event']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scan_added': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Scan']", 'on_delete': 'models.PROTECT'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Status']", 'on_delete': 'models.PROTECT'})
        },
        'prepa.area': {
            'Meta': {'object_name': 'Area'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'scan_added': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Scan']", 'on_delete': 'models.PROTECT'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Town']", 'on_delete': 'models.PROTECT'})
        },
        'prepa.event': {
            'Meta': {'object_name': 'Event'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Area']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scan_added': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added'", 'on_delete': 'models.PROTECT', 'to': "orm['prepa.Scan']"}),
            'scan_last_seen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_seen'", 'on_delete': 'models.PROTECT', 'to': "orm['prepa.Scan']"})
        },
        'prepa.scan': {
            'Meta': {'object_name': 'Scan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_breakdowns': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'num_towns': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'record_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'prepa.status': {
            'Meta': {'object_name': 'Status'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'scan_added': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Scan']", 'on_delete': 'models.PROTECT'})
        },
        'prepa.town': {
            'Meta': {'object_name': 'Town'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'scan_added': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Scan']", 'on_delete': 'models.PROTECT'})
        }
    }

    complete_apps = ['prepa']