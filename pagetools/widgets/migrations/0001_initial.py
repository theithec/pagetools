# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WidgetAdapter'
        db.create_table('widgets_widgetadapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('widgets', ['WidgetAdapter'])

        # Adding model 'ContentWidget'
        db.create_table('widgets_contentwidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('widgets', ['ContentWidget'])

        # Adding model 'TemplateTagWidget'
        db.create_table('widgets_templatetagwidget', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('name', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('renderclasskey', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('widgets', ['TemplateTagWidget'])

        # Adding model 'PageType'
        db.create_table('widgets_pagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['widgets.PageType'], null=True, blank=True)),
        ))
        db.send_create_signal('widgets', ['PageType'])

        # Adding model 'TypeArea'
        db.create_table('widgets_typearea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['widgets.PageType'])),
        ))
        db.send_create_signal('widgets', ['TypeArea'])

        # Adding model 'WidgetInArea'
        db.create_table('widgets_widgetinarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('typearea', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['widgets.TypeArea'])),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(related_name='widget_in_area', to=orm['widgets.WidgetAdapter'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('widgets', ['WidgetInArea'])


    def backwards(self, orm):
        # Deleting model 'WidgetAdapter'
        db.delete_table('widgets_widgetadapter')

        # Deleting model 'ContentWidget'
        db.delete_table('widgets_contentwidget')

        # Deleting model 'TemplateTagWidget'
        db.delete_table('widgets_templatetagwidget')

        # Deleting model 'PageType'
        db.delete_table('widgets_pagetype')

        # Deleting model 'TypeArea'
        db.delete_table('widgets_typearea')

        # Deleting model 'WidgetInArea'
        db.delete_table('widgets_widgetinarea')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'widgets.contentwidget': {
            'Meta': {'object_name': 'ContentWidget'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'widgets.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['widgets.PageType']", 'null': 'True', 'blank': 'True'})
        },
        'widgets.templatetagwidget': {
            'Meta': {'object_name': 'TemplateTagWidget'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'renderclasskey': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        'widgets.typearea': {
            'Meta': {'object_name': 'TypeArea'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['widgets.PageType']"}),
            'widgets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['widgets.WidgetAdapter']", 'through': "orm['widgets.WidgetInArea']", 'symmetrical': 'False'})
        },
        'widgets.widgetadapter': {
            'Meta': {'object_name': 'WidgetAdapter'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'widgets.widgetinarea': {
            'Meta': {'ordering': "['position']", 'object_name': 'WidgetInArea'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'typearea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['widgets.TypeArea']"}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'widget_in_area'", 'to': "orm['widgets.WidgetAdapter']"})
        }
    }

    complete_apps = ['widgets']
