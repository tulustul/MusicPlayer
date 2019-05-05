class Clipboard:

    instance = None

    def __init__(self):
        self.data = None

    @classmethod
    def get_instance(cls) -> 'Clipboard':
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def put(self, data):
        self.data = data

    def get(self):
        return self.data
