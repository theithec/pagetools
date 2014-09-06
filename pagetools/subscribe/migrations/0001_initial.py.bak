# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subscriber'
        db.create_table(u'subscribe_subscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_activated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subscribtion_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 14, 0, 0))),
            ('failures', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('key', self.gf('django.db.models.fields.CharField')(default='hIUrfWjlGcjilbZWZVpRmCpBTSirUSi', max_length=32)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal(u'subscribe', ['Subscriber'])

        # Adding model 'QueuedEmail'
        db.create_table(u'subscribe_queuedemail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('createdate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 14, 0, 0), blank=True)),
            ('modifydate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 14, 0, 0), blank=True)),
            ('senddate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 14, 0, 0), blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'subscribe', ['QueuedEmail'])

        # Adding model 'SendStatus'
        db.create_table(u'subscribe_sendstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscribe.Subscriber'])),
            ('queued_email', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscribe.QueuedEmail'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'subscribe', ['SendStatus'])


    def backwards(self, orm):
        # Deleting model 'Subscriber'
        db.delete_table(u'subscribe_subscriber')

        # Deleting model 'QueuedEmail'
        db.delete_table(u'subscribe_queuedemail')

        # Deleting model 'SendStatus'
        db.delete_table(u'subscribe_sendstatus')


    models = {
        u'subscribe.queuedemail': {
            'Meta': {'object_name': 'QueuedEmail'},
            'body': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'createdate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 14, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modifydate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 14, 0, 0)', 'blank': 'True'}),
            'senddate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 14, 0, 0)', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        u'subscribe.sendstatus': {
            'Meta': {'object_name': 'SendStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'queued_email': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['subscribe.QueuedEmail']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['subscribe.Subscriber']"})
        },
        u'subscribe.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'failures': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'CWFbZ6EZ9ZNXOawBiFZs5MmHEv0J96m'", 'max_length': '32'}),
            'subscribtion_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 14, 0, 0)'})
        }
    }

    complete_apps = ['subscribe']
