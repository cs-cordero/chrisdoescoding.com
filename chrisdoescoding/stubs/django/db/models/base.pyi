from typing import Type

class ModelBase(type): ...

class Model(metaclass=ModelBase):
    pk: int
    id: int
    DoesNotExist: Type[Exception]
