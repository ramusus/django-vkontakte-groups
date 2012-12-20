from ajax_select import LookupChannel
from models import Group

class VkontakteLookupChannel(LookupChannel):

    def get_pk(self,obj):
        return getattr(obj,'remote_id')

    def get_objects(self, ids):
        ids = [int(id) for id in ids]
        return self.model.objects.filter(remote_id__in=ids)

class GroupLookup(VkontakteLookupChannel):
    model = Group

    def get_query(self, q, request):
        return self.model.remote.search(q=q)

    def format_item_display(self, obj):
        return unicode(u'<a href="%s" target="_blank">%s</a>' % (obj.remote_link(), obj.name))