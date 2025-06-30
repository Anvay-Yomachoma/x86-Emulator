"""Core CPU state and memory model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

MEMORY_SIZE = 1024 * 1024  # 1 MB for demos
STACK_SIZE = 0x1000
STACK_BASE = MEMORY_SIZE - STACK_SIZE


@dataclass
class CPUState:
    regs: Dict[str, int] = field(default_factory=lambda: {
        "EAX": 0,
        "EBX": 0,
        "ECX": 0,
        "EDX": 0,
        "ESI": 0,
        "EDI": 0,
        "EBP": 0,
        "ESP": STACK_BASE,
        "EIP": 0,
        "EFLAGS": 0,
    })
    memory: bytearray = field(default_factory=lambda: bytearray(MEMORY_SIZE))
    labels: Dict[str, int] = field(default_factory=dict)
    instructions: List[Dict] = field(default_factory=list)

    def push(self, value: int) -> None:
        self.regs["ESP"] -= 4
        self._write_dword(self.regs["ESP"], value)

    def pop(self) -> int:
        value = self._read_dword(self.regs["ESP"])
        self.regs["ESP"] += 4
        return value

    def _write_dword(self, addr: int, value: int) -> None:
        self.memory[addr:addr+4] = value.to_bytes(4, "little")

    def _read_dword(self, addr: int) -> int:
        return int.from_bytes(self.memory[addr:addr+4], "little")

    def fetch_instruction(self) -> Dict:
        try:
            ins = self.instructions[self.regs["EIP"]]
        except IndexError:
            raise StopIteration("EIP out of range")
        self.regs["EIP"] += 1
        return ins
