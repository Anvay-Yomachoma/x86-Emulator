from emulator.core import CPUState
from emulator.debugger import Debugger


def test_step():
    cpu = CPUState()
    cpu.instructions = [{"op": "MOV", "args": ["EAX", "1"], "text": "MOV EAX, 1"}]
    dbg = Debugger(cpu)
    dbg.step()
    assert cpu.regs["EAX"] == 1
