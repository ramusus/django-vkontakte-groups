import factory

from .models import Group


class GroupFactory(factory.DjangoModelFactory):

    remote_id = factory.Sequence(lambda n: n)

    class Meta:
        model = Group
