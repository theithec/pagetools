# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GalleryPic'
        db.create_table(u'gallery_gallerypic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('pic', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'gallery', ['GalleryPic'])

        # Adding model 'Gallery'
        db.create_table(u'gallery_gallery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('status', self.gf('model_utils.fields.StatusField')(default='draft', max_length=100, no_check_for_status=True)),
            ('status_changed', self.gf('model_utils.fields.MonitorField')(default=datetime.datetime.now, monitor=u'status')),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal(u'gallery', ['Gallery'])

        # Adding model 'PicPos'
        db.create_table(u'gallery_picpos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='picpospic', to=orm['gallery.GalleryPic'])),
            ('gal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Gallery'])),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'gallery', ['PicPos'])


    def backwards(self, orm):
        # Deleting model 'GalleryPic'
        db.delete_table(u'gallery_gallerypic')

        # Deleting model 'Gallery'
        db.delete_table(u'gallery_gallery')

        # Deleting model 'PicPos'
        db.delete_table(u'gallery_picpos')


    models = {
        u'gallery.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'pics': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gallery.GalleryPic']", 'through': u"orm['gallery.PicPos']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'gallery.gallerypic': {
            'Meta': {'object_name': 'GalleryPic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'gallery.picpos': {
            'Meta': {'object_name': 'PicPos'},
            'gal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gallery.Gallery']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'picpospic'", 'to': u"orm['gallery.GalleryPic']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['gallery']
