# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Group'
        db.create_table('vkontakte_groups_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remote_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('photo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('photo_medium', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('photo_big', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('vkontakte_groups', ['Group'])

        # Adding model 'GroupStat'
        db.create_table('vkontakte_groups_groupstat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='statistics', to=orm['vkontakte_groups.Group'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('visitors', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('views', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('likes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('comments', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('shares', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('new_members', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ex_members', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('members', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ads_visitors', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('ads_members', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('males', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('females', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('vkontakte_groups', ['GroupStat'])

        # Adding unique constraint on 'GroupStat', fields ['group', 'time']
        db.create_unique('vkontakte_groups_groupstat', ['group_id', 'time'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'GroupStat', fields ['group', 'time']
        db.delete_unique('vkontakte_groups_groupstat', ['group_id', 'time'])

        # Deleting model 'Group'
        db.delete_table('vkontakte_groups_group')

        # Deleting model 'GroupStat'
        db.delete_table('vkontakte_groups_groupstat')


    models = {
        'vkontakte_groups.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo_big': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo_medium': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'vkontakte_groups.groupstat': {
            'Meta': {'ordering': "('group', 'time')", 'unique_together': "(('group', 'time'),)", 'object_name': 'GroupStat'},
            'ads_members': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ads_visitors': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'comments': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'ex_members': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'females': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'statistics'", 'to': "orm['vkontakte_groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'males': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'members': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'new_members': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'shares': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'visitors': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['vkontakte_groups']
