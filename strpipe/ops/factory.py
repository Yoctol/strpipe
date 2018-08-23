from .pad import Pad


class _OpFactory:

    def __init__(self):
        self._factory = {}

    def register(self, name, op_class):
        if name not in self._factory:
            self._factory[name] = op_class
        else:
            raise KeyError(f"{name} already exists.")


op_factory = _OpFactory()

op_factory.register('Pad'
    Pad,
)
