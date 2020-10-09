from unittest import TestCase

from pcom.commands import datatables


class BaseTest(TestCase):
    def setUp(self) -> None:
        self._columns = [
            datatables.Byte(),
            datatables.String(5),
            datatables.ULong(),
            datatables.Bool(9),
            datatables.Bool(),
            datatables.Bool(),
            datatables.Int(2),
            datatables.Byte()
        ]
        self._structure = datatables.DatatableStructure("Some table", offset=44, rows=22, columns=self._columns)
