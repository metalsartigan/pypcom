# PCOM #

A very basic Unitronics PCOM protocol implementation in Python.

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
