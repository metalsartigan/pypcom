from .ascii_command import AsciiCommand


class AsciiWriteCommand(AsciiCommand):
    def parse_reply(self, buffer: bytearray) -> bool:
        buffer = super().parse_reply(buffer).decode()
        return buffer == ''
