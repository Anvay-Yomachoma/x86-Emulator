from emulator.core import CPUState


def test_push_pop():
    cpu = CPUState()
    cpu.push(0x12345678)
    assert cpu.pop() == 0x12345678
