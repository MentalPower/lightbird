# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Action.scan_last_seen'
        db.add_column('prepa_action', 'scan_last_seen',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='action_last_seen', on_delete=models.PROTECT, to=orm['prepa.Scan']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Action.scan_last_seen'
        db.delete_column('prepa_action', 'scan_last_seen_id')


    models = {
        'prepa.action': {
            'Meta': {'unique_together': "(('event', 'status'),)", 'object_name': 'Action'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['prepa.Event']", 'on_delete': 'models.PROTECT'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scan_added': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'action_added'", 'on_delete': 'models.PROTECT', 'to': "orm['prepa.Scan']"}),
            'scan_last_seen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'action_last_seen'", 'on_delete': 'models.PROTECT', 'to': "orm['prepa.Scan']"}),
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
            'scan_added': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_added'", 'on_delete': 'models.PROTECT', 'to': "orm['prepa.Scan']"}),
            'scan_last_seen': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event_last_seen'", 'on_delete': 'models.PROTECT', 'to': "orm['prepa.Scan']"})
        },
        'prepa.scan': {
            'Meta': {'object_name': 'Scan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_breakdowns': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'num_towns': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'record_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_taken': ('django.db.models.fields.FloatField', [], {'default': '0'})
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
