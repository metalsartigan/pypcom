# PCOM #

A very basic Unitronics PCOM protocol implementation for Python 3.


### How to use ###
```
from pcom import commands
from pcom.plc import EthernetPlc

with EthernetPlc(address=('192.168.5.43', 1616)) as plc:
    # Read realtime clock
    c = commands.ReadRtc()
    res = plc.send(c)
    print(res)
    
    # Set realtime clock
    c = commands.SetRtc(value=datetime.now())
    plc.send(c)
    
    # Set MB 300 through 304
    values = [True, False, True, True, False]
    c = commands.SetBits(code=commands.SetBits.MEMORY, address=300, values=values)
    plc.send(c)
```
When entering the `with` block, the `plc` instance connects to the PLC
and the connection is closed when the block is done, or when an error occurs
within the block.

You can also manually call the `connect()` and `close()` methods:

```
from pcom import commands
from pcom.plc import EthernetPlc

plc = EthernetPlc(address=('192.168.5.43', 1616))
try:
  plc.connect()
  # Read realtime clock
  c = commands.ReadRtc()
  res = plc.send(c)
  print(res)
finally:  # Always close the connection.
  plc.close()
```

See the `commands` Python package for available commands.

Datatable commands are in the `commands.datatables` package.
To work with a datatable, its structure has to be defined.
Here's an example:

```
from pcom import commands
from pcom.plc import EthernetPlc


with EthernetPlc(address=('192.168.5.47', 1616)) as plc:
    table_structure = commands.datatables.DatatableStructure("My table", offset=19000, rows=2, columns=[
        commands.datatables.Int(),
        commands.datatables.Int(2),
        commands.datatables.Int(),
        commands.datatables.Int(),
        commands.datatables.Long(),
    ])
    c = commands.datatables.ReadDatatable(structure=table_structure, row_count=2)
    res = plc.send(c)
    print('My table', res)
```

Writing to a datatable is very much alike:

```
from pcom import commands
from pcom.plc import EthernetPlc


with EthernetPlc(address=('192.168.5.47', 1616)) as plc:
    table_structure = commands.datatables.DatatableStructure("My table", offset=19000, rows=2, columns=[
        commands.datatables.Int(2),
        commands.datatables.Int(),
        commands.datatables.String(5),
        commands.datatables.Int(),
        commands.datatables.Int(),
        commands.datatables.Long(),
    ])

    rows = [
        [[11, 12], [13], "hello", [14], [15], [-673542]],
        [[11, 14], [15], "bye  ", [16], [17], [655666]],
    ]
    c = commands.datatables.WriteDatatable(structure=table_structure, data=rows)
    try:
        plc.send(c)
    except datatables.WriteDatatableError as ex:
        print(ex)
```

### Known limitations ###
- General:
    - Serial communication is not implemented yet.
- Datatables:
    - "Part of project" columns are not supported.
    - Reading a datatable structure is not supported.


### Changelog  ###
#### Version 0.8 ####
- Start of changelog
- BREAKING: Methods _connect() and _close() have been renamed to connect() and close().
Unless you have subclasses that overrides those methods, this has no impact.
