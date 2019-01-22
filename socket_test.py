from pcom import commands
from pcom.plc import EthernetPlc
import time

from datetime import datetime

with EthernetPlc(address=('192.168.5.43', 1616)) as plc:
    c2 = commands.ID()

    values = [True, False, True, True, False]

    run = True
    count = 0
    while run:
        count += 1
        #c = commands.SetBits(code=commands.SetBits.MEMORY, address=300, values=values)
        c = commands.SetRtc(value=datetime.now())
        #c = commands.SetRtc(value=datetime(2018, 12, 13, 14, 43, 10))

        res = plc.send(c)
        print(res)

        print('request number:', count)
        run = False

        for i in range(len(values)):
            values[i] = not values[i]

        if run:
            time.sleep(1)

