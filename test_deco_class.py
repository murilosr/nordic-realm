from app.models.test import Test
from app.repositories.test_repository import TestRepository
from nordic_realm.MongoBaseModel import MongoBaseModel

t = TestRepository()

from inspect import signature
for _k in dir(TestRepository):
    print(_k, getattr(TestRepository, _k, None))
    
print("\n\n\n")
print(TestRepository.__orig_bases__[0].__args__[0])

id_class = TestRepository.__orig_bases__[0].__args__[0]

test = type(id_class.__name__, (id_class, ), {})
print(type(test))
print(test(x=999))

print(Test(x = 999))