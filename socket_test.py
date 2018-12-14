from pcom.commands import CommandID
from pcom.models import EthernetPcomPlc

with EthernetPcomPlc(address=('192.168.5.43', 20256)) as plc:
    plc.connect()
    c = CommandID()
    res = plc.send(c)
    print(res)

