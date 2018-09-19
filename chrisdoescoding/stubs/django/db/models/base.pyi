from typing import Type


class ModelBase(type): ...
class Model(metaclass=ModelBase):
    id: int
    DoesNotExist: Type[Exception]
