from pcom import commands
from pcom.commands import operand_request
from pcom.plc import EthernetPlc
import time

with EthernetPlc(address=('192.168.5.43', 20256)) as plc:
    c2 = commands.CommandID()

    values = [True, False, True, True, False]

    run = True
    count = 0
    while run:
        count += 1
        c = commands.CommandSetBits(code=commands.CommandSetBits.MEMORY, address=300, values=values)
        res = plc.send(c)
        print(res)

        print('request number:', count)
        run = True

        for i in range(len(values)):
            values[i] = not values[i]

        if run:
            time.sleep(1)

