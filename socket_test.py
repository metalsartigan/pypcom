from pcom import commands
from pcom.plc import EthernetPlc


with EthernetPlc(address=('192.168.5.47', 1616)) as plc:
    #c = commands.SetBits(code=commands.SetBits.MEMORY, address=300, values=values)
    #c = commands.SetRtc(value=datetime.now())
    #c = commands.SetRtc(value=datetime(2018, 12, 13, 14, 43, 10))
    if False:
        test_structure = commands.datatables.DatatableStructure("Test", offset=20200, rows=2, columns=[
            commands.datatables.String(5),
            commands.datatables.Float(),
            commands.datatables.Timer(),
            commands.datatables.ULong(),
            commands.datatables.Long(),
            commands.datatables.UInt(),
            commands.datatables.Int(),
            commands.datatables.Byte(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
        ])
        c = commands.datatables.ReadDatatable(structure=test_structure, row_count=2)
        res = plc.send(c)
        print('test', res)

    if False:

        poids_structure = commands.datatables.DatatableStructure("Poids", offset=19000, rows=2, columns=[
            commands.datatables.Int(),
            commands.datatables.Int(),
            commands.datatables.Int(),
            commands.datatables.Int(),
            commands.datatables.Long(),
        ])
        c = commands.datatables.ReadDatatable(structure=poids_structure, row_count=2)
        res = plc.send(c)
        print('poids', res)
        print()

    if True:
        table1_structure = commands.datatables.DatatableStructure("Table1", offset=0, rows=2, columns=[
            commands.datatables.ULong(),
            commands.datatables.ULong(),
            commands.datatables.ULong(),
            commands.datatables.Bool(),
            commands.datatables.Long(),
            commands.datatables.Long(),
            commands.datatables.Long(),
            commands.datatables.Int(),
            commands.datatables.Int(),
            commands.datatables.Int(),
            commands.datatables.Byte(),
            commands.datatables.Int(),
            commands.datatables.Int(),
            commands.datatables.Bool(),
            commands.datatables.Bool(),
        ])
        c = commands.datatables.ReadDatatable(structure=table1_structure, row_count=2)
        res = plc.send(c)
        print('table1', res)
