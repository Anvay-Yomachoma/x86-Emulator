"""Debugger and execution engine."""

from __future__ import annotations

from typing import Dict, List, Set

from .core import CPUState
from .instructions import INSTRUCTION_SET
from .conventions import handle_call


class Debugger:
    def __init__(self, cpu: CPUState) -> None:
        self.cpu = cpu
        self.breakpoints: Set[int] = set()
        self.running = True

    def step(self) -> None:
        ins = self.cpu.fetch_instruction()
        op = ins["op"]
        args = ins["args"]
        if op == "CALL" and ins["args"][0] not in self.cpu.labels:
            handle_call(self.cpu, ins["args"][0])
            return
        func = INSTRUCTION_SET.get(op)
        if not func:
            raise ValueError(f"Unknown instruction: {op}")
        func(self.cpu, args)

    def continue_run(self) -> None:
        while self.running:
            if self.cpu.regs["EIP"] in self.breakpoints:
                break
            try:
                self.step()
            except StopIteration:
                self.running = False
                break

    def add_breakpoint(self, addr: int) -> None:
        self.breakpoints.add(addr)

    def dump_registers(self) -> Dict[str, int]:
        return dict(self.cpu.regs)

    def dump_stack(self, words: int = 4) -> List[int]:
        addr = self.cpu.regs["ESP"]
        return [self.cpu._read_dword(addr + i * 4) for i in range(words)]
