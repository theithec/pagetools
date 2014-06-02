# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageDynFormField'
        db.create_table(u'pages_pagedynformfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('required', self.gf('django.db.models.fields.BooleanField')()),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('initial', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
        ))
        db.send_create_signal(u'pages', ['PageDynFormField'])


    def backwards(self, orm):
        # Deleting model 'PageDynFormField'
        db.delete_table(u'pages_pagedynformfield')


    models = {
        u'pages.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_form': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'pagetype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['widgets.PageType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('pagetools.core.unislug.models.UnicodeSlugField', [], {'max_length': '255'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pages.pagedynformfield': {
            'Meta': {'ordering': "['position']", 'object_name': 'PageDynFormField'},
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'required': ('django.db.models.fields.BooleanField', [], {})
        },
        u'widgets.pagetype': {
            'Meta': {'object_name': 'PageType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['widgets.PageType']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pages']