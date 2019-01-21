from pcom.commands import CommandID, CommandReadOperands
from pcom.commands import operand_request
from pcom.plc import EthernetPlc

with EthernetPlc(address=('192.168.5.43', 20256)) as plc:
    c2 = CommandID()
    c = CommandReadOperands()

    requests = [
        operand_request.MB(addresses=[78]),
        operand_request.MB(addresses=[34], length=6),
        operand_request.Input(addresses=[7], length=9),
        operand_request.Input(addresses=[65]),
        operand_request.TimerRunBit(addresses=[34, 129]),
        operand_request.TimerRunBit(addresses=[42], length=6),
        operand_request.CounterRunBit(addresses=[15]),
        operand_request.CounterRunBit(addresses=[6], length=4),
        operand_request.MI(addresses=[17, 19]),
        operand_request.MI(addresses=[1022], length=6),
        operand_request.TimerCurrent(addresses=[34, 129]),
        operand_request.TimerPreset(addresses=[34, 129]),
        operand_request.TimerCurrent(addresses=[42], length=6),
        operand_request.TimerPreset(addresses=[42], length=6),
        operand_request.ML(addresses=[13]),
        operand_request.DW(addresses=[12], length=3),
        operand_request.CounterCurrent(addresses=[15]),
        operand_request.CounterPreset(addresses=[15]),
        operand_request.CounterCurrent(addresses=[6], length=4),
        operand_request.CounterPreset(addresses=[6], length=4),
        operand_request.MF(addresses=[6]),
        operand_request.MF(addresses=[9], length=4)
    ]
    for request in requests:
        c.add_request(request)

    res = plc.send(c)
    print(res)

    for request in requests:
        print(request.values)
