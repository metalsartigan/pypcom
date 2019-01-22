class PComError(Exception):
    def __init__(self, *args, data=None, **kwargs):
        self.data = data
        super().__init__(*args, **kwargs)
