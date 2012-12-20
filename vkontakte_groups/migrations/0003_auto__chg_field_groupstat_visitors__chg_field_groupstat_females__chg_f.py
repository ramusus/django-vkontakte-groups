# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'GroupStat.visitors'
        db.alter_column('vkontakte_groups_groupstat', 'visitors', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.females'
        db.alter_column('vkontakte_groups_groupstat', 'females', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.views'
        db.alter_column('vkontakte_groups_groupstat', 'views', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.ads_visitors'
        db.alter_column('vkontakte_groups_groupstat', 'ads_visitors', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.males'
        db.alter_column('vkontakte_groups_groupstat', 'males', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.ads_members'
        db.alter_column('vkontakte_groups_groupstat', 'ads_members', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.comments'
        db.alter_column('vkontakte_groups_groupstat', 'comments', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.ex_members'
        db.alter_column('vkontakte_groups_groupstat', 'ex_members', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.shares'
        db.alter_column('vkontakte_groups_groupstat', 'shares', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.members'
        db.alter_column('vkontakte_groups_groupstat', 'members', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.new_members'
        db.alter_column('vkontakte_groups_groupstat', 'new_members', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

        # Changing field 'GroupStat.likes'
        db.alter_column('vkontakte_groups_groupstat', 'likes', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))


    def backwards(self, orm):

        # Changing field 'GroupStat.visitors'
        db.alter_column('vkontakte_groups_groupstat', 'visitors', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.females'
        db.alter_column('vkontakte_groups_groupstat', 'females', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.views'
        db.alter_column('vkontakte_groups_groupstat', 'views', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.ads_visitors'
        db.alter_column('vkontakte_groups_groupstat', 'ads_visitors', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.males'
        db.alter_column('vkontakte_groups_groupstat', 'males', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.ads_members'
        db.alter_column('vkontakte_groups_groupstat', 'ads_members', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.comments'
        db.alter_column('vkontakte_groups_groupstat', 'comments', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.ex_members'
        db.alter_column('vkontakte_groups_groupstat', 'ex_members', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.shares'
        db.alter_column('vkontakte_groups_groupstat', 'shares', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.members'
        db.alter_column('vkontakte_groups_groupstat', 'members', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.new_members'
        db.alter_column('vkontakte_groups_groupstat', 'new_members', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

        # Changing field 'GroupStat.likes'
        db.alter_column('vkontakte_groups_groupstat', 'likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))


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
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'vkontakte_groups.groupstat': {
            'Meta': {'ordering': "('group', 'time')", 'unique_together': "(('group', 'time'),)", 'object_name': 'GroupStat'},
            'ads_members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'ads_visitors': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'comments': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'ex_members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'females': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'statistics'", 'to': "orm['vkontakte_groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'males': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'new_members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'shares': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'visitors': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['vkontakte_groups']
