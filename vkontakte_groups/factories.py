from models import Group
import factory

class GroupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Group

    remote_id = factory.Sequence(lambda n: n)
    is_closed = False