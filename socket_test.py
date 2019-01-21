from pcom import commands
from pcom.commands import operand_request
from pcom.plc import EthernetPlc
import time

def do_request():
    with EthernetPlc(address=('192.168.5.43', 20256)) as plc:
        c2 = commands.CommandID()

        c = commands.CommandReadRtc()

        res = plc.send(c)
        print(res)


run = True
i = 0
while run:
    i += 1
    do_request()
    print('request number:', i)
    #run = False
    time.sleep(1)
