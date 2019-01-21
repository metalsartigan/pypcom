from pcom.commands import CommandID, CommandReadOperands
from pcom.commands.command_read_operands import MB, MI, INPUT, TIMER_RUN_BIT, MF, COUNTER_RUN_BIT, TIMER_CURRENT, TIMER_PRESET, ML, DW, COUNTER_CURRENT, COUNTER_PRESET
from pcom.plc import EthernetPlc

with EthernetPlc(address=('google.com', 80)) as plc:
    #c = CommandID()
    c = CommandReadOperands()

    c.add_request(operand_type=MB, addresses=[78])
    c.add_request(operand_type=MB, addresses=[34], length=6)
    c.add_request(operand_type=INPUT, addresses=[7], length=9)
    c.add_request(operand_type=INPUT, addresses=[65])
    c.add_request(operand_type=TIMER_RUN_BIT, addresses=[34, 129])
    c.add_request(operand_type=TIMER_RUN_BIT, addresses=[42], length=6)  # 8B
    c.add_request(operand_type=COUNTER_RUN_BIT, addresses=[15])
    c.add_request(operand_type=COUNTER_RUN_BIT, addresses=[6], length=4)  # 8C
    c.add_request(operand_type=MI, addresses=[17, 19])
    c.add_request(operand_type=MI, addresses=[1022], length=6)
    c.add_request(operand_type=TIMER_CURRENT, addresses=[34, 129])
    c.add_request(operand_type=TIMER_PRESET, addresses=[34, 129])
    c.add_request(operand_type=TIMER_CURRENT, addresses=[42], length=6)  # 94
    c.add_request(operand_type=TIMER_PRESET, addresses=[42], length=6)  # 95
    c.add_request(operand_type=ML, addresses=[13])
    c.add_request(operand_type=DW, addresses=[12], length=3)
    c.add_request(operand_type=COUNTER_CURRENT, addresses=[15])
    c.add_request(operand_type=COUNTER_PRESET, addresses=[15])
    c.add_request(operand_type=COUNTER_CURRENT, addresses=[6], length=4)  # 92
    c.add_request(operand_type=COUNTER_PRESET, addresses=[6], length=4)  # 93
    c.add_request(operand_type=MF, addresses=[6])
    c.add_request(operand_type=MF, addresses=[9], length=4)


    res = plc.send(c)
    print(res)
