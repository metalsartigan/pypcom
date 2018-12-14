from pcom.models import AsciiCommand


class CommandID(AsciiCommand):
    def __init__(self):
        super().__init__(code='ID')
