"""Instruction implementations."""

from __future__ import annotations

from typing import Dict, Callable, List

from .core import CPUState
from .utils import parse_number


InstructionFunc = Callable[[CPUState, List[str]], None]


REGISTERS = {
    "EAX", "EBX", "ECX", "EDX", "ESI", "EDI", "EBP", "ESP", "EIP",
}


def _get_operand_value(cpu: CPUState, op: str) -> int:
    op = op.upper()
    if op in cpu.regs:
        return cpu.regs[op]
    return parse_number(op)


def _set_register(cpu: CPUState, reg: str, value: int) -> None:
    cpu.regs[reg.upper()] = value & 0xFFFFFFFF


def mov(cpu: CPUState, args: List[str]) -> None:
    dst, src = args
    value = _get_operand_value(cpu, src)
    _set_register(cpu, dst, value)


def add(cpu: CPUState, args: List[str]) -> None:
    dst, src = args
    value = _get_operand_value(cpu, src)
    _set_register(cpu, dst, (cpu.regs[dst.upper()] + value) & 0xFFFFFFFF)


def sub(cpu: CPUState, args: List[str]) -> None:
    dst, src = args
    value = _get_operand_value(cpu, src)
    _set_register(cpu, dst, (cpu.regs[dst.upper()] - value) & 0xFFFFFFFF)


def jmp(cpu: CPUState, args: List[str]) -> None:
    target = args[0]
    if target in cpu.labels:
        cpu.regs["EIP"] = cpu.labels[target]
    else:
        cpu.regs["EIP"] = _get_operand_value(cpu, target)


def cmp(cpu: CPUState, args: List[str]) -> None:
    a = _get_operand_value(cpu, args[0])
    b = _get_operand_value(cpu, args[1])
    cpu.regs["EFLAGS"] = 0
    if a == b:
        cpu.regs["EFLAGS"] |= 0x40  # ZF


def je(cpu: CPUState, args: List[str]) -> None:
    if cpu.regs["EFLAGS"] & 0x40:
        jmp(cpu, args)


def jne(cpu: CPUState, args: List[str]) -> None:
    if not (cpu.regs["EFLAGS"] & 0x40):
        jmp(cpu, args)


def call(cpu: CPUState, args: List[str]) -> None:
    target = args[0]
    cpu.push(cpu.regs["EIP"])  # push return addr
    if target in cpu.labels:
        cpu.regs["EIP"] = cpu.labels[target]
    else:
        # external call stub
        print(f"[call] external function '{target}'")
        cpu.pop()  # discard return


def ret(cpu: CPUState, args: List[str]) -> None:
    cpu.regs["EIP"] = cpu.pop()


def nop(cpu: CPUState, args: List[str]) -> None:
    pass


INSTRUCTION_SET: Dict[str, InstructionFunc] = {
    "MOV": mov,
    "ADD": add,
    "SUB": sub,
    "JMP": jmp,
    "CMP": cmp,
    "JE": je,
    "JNE": jne,
    "CALL": call,
    "RET": ret,
    "NOP": nop,
}
