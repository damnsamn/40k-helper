import state

class ClassFactory:
    """Construct a new class with members matching the key-value pairs of the provided data"""
    def __init__(self, data:dict):
        for key, value in data.items():
            setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

class Wargear(ClassFactory):
    def __init__(self, data):
        ClassFactory.__init__(self, data)

class Model(ClassFactory):
    def __init__(self, data):
        ClassFactory.__init__(self, data)
        self.wargear: list[Wargear] = []


