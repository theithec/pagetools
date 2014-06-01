# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WidgetAdapter'
        db.delete_table(u'widgets_widgetadapter')

        # Adding unique constraint on 'TypeArea', fields ['area', 'type', 'lang']
        db.create_unique(u'widgets_typearea', ['area', 'type_id', 'lang'])

        # Deleting field 'WidgetInArea.widget'
        db.delete_column(u'widgets_widgetinarea', 'widget_id')

        # Adding field 'WidgetInArea.content_type'
        db.add_column(u'widgets_widgetinarea', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['contenttypes.ContentType']),
                      keep_default=False)

        # Adding field 'WidgetInArea.object_id'
        db.add_column(u'widgets_widgetinarea', 'object_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'TypeArea', fields ['area', 'type', 'lang']
        db.delete_unique(u'widgets_typearea', ['area', 'type_id', 'lang'])

        # Adding model 'WidgetAdapter'
        db.create_table(u'widgets_widgetadapter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'widgets', ['WidgetAdapter'])

        # Adding field 'WidgetInArea.widget'
        db.add_column(u'widgets_widgetinarea', 'widget',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='widget_in_area', to=orm['widgets.WidgetAdapter']),
                      keep_default=False)

        # Deleting field 'WidgetInArea.content_type'
        db.delete_column(u'widgets_widgetinarea', 'content_type_id')

        # Deleting field 'WidgetInArea.object_id'
        db.delete_column(u'widgets_widgetinarea', 'object_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'widgets.contentwidget': {
            'Meta': {'object_name': 'ContentWidget'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        u'widgets.pagetype': {
            'Meta': {'object_name': 'PageType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['widgets.PageType']", 'null': 'True', 'blank': 'True'})
        },
        u'widgets.templatetagwidget': {
            'Meta': {'object_name': 'TemplateTagWidget'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'renderclasskey': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'})
        },
        u'widgets.typearea': {
            'Meta': {'unique_together': "(('area', 'type', 'lang'),)", 'object_name': 'TypeArea'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['widgets.PageType']"})
        },
        u'widgets.widgetinarea': {
            'Meta': {'ordering': "['position']", 'object_name': 'WidgetInArea'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'typearea': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['widgets.TypeArea']"})
        }
    }

    complete_apps = ['widgets']