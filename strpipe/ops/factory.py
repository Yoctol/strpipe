class _OpFactory:

    def __init__(self):
        self._factory = {}

    def register(self, name, op_class):
        if name not in self._factory:
            self._factory[name] = op_class
        else:
            raise KeyError(f"{name} already exists.")

    def __getitem__(self, op_name):
        if op_name not in self._factory:
            raise KeyError(f"{op_name} is not registered")
        return self._factory[op_name]
