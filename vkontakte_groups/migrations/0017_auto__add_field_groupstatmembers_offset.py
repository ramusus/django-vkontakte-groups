# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'GroupStatMembers.offset'
        db.add_column('vkontakte_groups_groupstatmembers', 'offset', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'GroupStatMembers.offset'
        db.delete_column('vkontakte_groups_groupstatmembers', 'offset')


    models = {
        'vkontakte_groups.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_big': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_medium': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['vkontakte_users.User']", 'symmetrical': 'False'})
        },
        'vkontakte_groups.groupstat': {
            'Meta': {'ordering': "('group', 'time')", 'unique_together': "(('group', 'time'),)", 'object_name': 'GroupStat'},
            'act_members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'act_visitors': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'activity_photo_comments': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'activity_photos': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'activity_topic_comments': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'activity_topics': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'activity_video_comments': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'activity_videos': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'activity_wall': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'ads_members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'ads_visitors': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'age_18': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'age_18_21': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'age_21_24': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'age_24_27': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'age_27_30': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'age_30_35': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'age_35_45': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'age_45': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'comments': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'ex_members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'females': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'statistics'", 'to': "orm['vkontakte_groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'males': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'new_members': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'section_applications': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'section_audio': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'section_discussions': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'section_documents': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'section_photoalbums': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'section_video': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'shares': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'visitors': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'vkontakte_groups.groupstatmembers': {
            'Meta': {'ordering': "('group', 'time', '-id')", 'unique_together': "(('group', 'time'),)", 'object_name': 'GroupStatMembers'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members_statistics'", 'to': "orm['vkontakte_groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.TextField', [], {}),
            'members_entered': ('django.db.models.fields.TextField', [], {}),
            'members_left': ('django.db.models.fields.TextField', [], {}),
            'offset': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'vkontakte_groups.groupstatpersentage': {
            'Meta': {'ordering': "('group', '-type', 'order')", 'unique_together': "(('group', 'type', 'value_type'),)", 'object_name': 'GroupStatPersentage', 'db_table': "'vkontakte_groups_groupstatpercentage'"},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'percentage_statistics'", 'to': "orm['vkontakte_groups.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'percents': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'value_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value_type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vkontakte_places.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cities'", 'null': 'True', 'to': "orm['vkontakte_places.Country']"}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_places.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'})
        },
        'vkontakte_users.user': {
            'Meta': {'ordering': "['remote_id']", 'object_name': 'User'},
            'activity': ('django.db.models.fields.TextField', [], {}),
            'albums': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'audios': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'bdate': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.City']", 'null': 'True'}),
            'counters_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vkontakte_places.Country']", 'null': 'True'}),
            'faculty': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'faculty_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'followers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'friends': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'graduation': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'has_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mutual_friends': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'notes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_big': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_medium': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_medium_rec': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'photo_rec': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'rate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'relation': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'remote_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.IntegerField', [], {}),
            'subscriptions': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'sum_counters': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'timezone': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'university': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'university_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user_photos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user_videos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'videos': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'wall_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['vkontakte_groups']
