from models import Group
import factory
import random

class GroupFactory(factory.Factory):
    FACTORY_FOR = Group

    remote_id = factory.Sequence(lambda n: n)