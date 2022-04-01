import sys

from pcom import commands
from pcom.plc import EthernetPlc
from datetime import timedelta


with EthernetPlc(address=('192.168.5.47', 1616)) as plc:
    if False:
        columns = [
            commands.datatables.ULong(3),  # employee, job, material
            commands.datatables.Bool(),  # begin / end
            commands.datatables.Long(3),  # weight, reserved, reserved
            commands.datatables.Int(3),  # year, day-month, hour-minutes
            commands.datatables.Byte(),  # seconds
            commands.datatables.Int(2),  # reserved, reserved
            commands.datatables.Bool(),  # reserved
            commands.datatables.Bool(),  # reserved
        ]
        structure = commands.datatables.DatatableStructure("Readings", offset=39200,
                                                              rows=500,
                                                              columns=columns)

        c = commands.datatables.ReadDatatable(structure=structure, row_count=25)
        res = plc.send(c)
        print('test', res)
    if True:
        cmd = commands.ReadOperands()
        cmd.add_request(commands.operand_request.MB(addresses=[10, 11, 12, 13, 14, 15, 16, 17, 18, 19]))
        x = plc.send(cmd)
        print('reply:', x[0].values)
    if False:
        cmd = commands.WriteFloats(address=30, values=[1, -10, 3.3])
        x = plc.send(cmd)
        print('reply:', x)

    if False:
        cols = [
            commands.datatables.Int(),  # Quantity
            commands.datatables.Long(),  # Length
            commands.datatables.Int(),  # length table #
            commands.datatables.Int(),  # width table #
        ]
        struct = commands.datatables.DatatableStructure("Recipe", offset=9760, rows=60,
                                                                              columns=cols)

        data = [[[2], [10333], [0], [0]], [[4], [12777], [1], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]], [[0], [0], [0], [0]]]
        cmd = commands.datatables.WriteDatatable(structure=struct, data=data)
        plc.send(cmd)

        # c = commands.SetBits(code=commands.SetBits.MEMORY, address=300, values=values)
        # c = commands.SetRtc(value=datetime.now())
        # c = commands.SetRtc(value=datetime(2018, 12, 13, 14, 43, 10))
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
        data = [
            [
                [timedelta(hours=6)]
            ],
            [
                [timedelta(hours=5)]
            ]
        ]
        c = commands.datatables.WriteDatatable(structure=test_structure, data=data, start_column_index=2)
        res = plc.send(c)
        print('test', res)

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
        c = commands.datatables.ReadDatatable(structure=test_structure, row_count=2, start_column_index=2, column_count=1)
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

    if False:
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
        print('table1')
        for r in res:
            print(r)
