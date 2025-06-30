"""Command line interface for the emulator."""

from __future__ import annotations

import argparse
import cmd
import shlex
from typing import List

from emulator.loader import load_file
from emulator.core import CPUState
from emulator.debugger import Debugger
from emulator.utils import parse_number, to_hex


class EmulatorShell(cmd.Cmd):
    intro = "x86 Emulator. Type help or ? to list commands."
    prompt = "(emu) "

    def __init__(self, dbg: Debugger):
        super().__init__()
        self.dbg = dbg

    def do_next(self, arg: str) -> bool:
        """Execute next instruction."""
        self.dbg.step()
        print(self.dbg.cpu.instructions[self.dbg.cpu.regs["EIP"] - 1]["text"])
        return False

    do_n = do_next

    def do_cont(self, arg: str) -> bool:
        """Continue execution."""
        self.dbg.continue_run()
        return False

    do_c = do_cont

    def do_regs(self, arg: str) -> bool:
        regs = self.dbg.dump_registers()
        for k, v in regs.items():
            print(f"{k}: {to_hex(v)}")
        return False

    def do_stack(self, arg: str) -> bool:
        words = int(arg) if arg else 4
        stack = self.dbg.dump_stack(words)
        for i, val in enumerate(stack):
            print(f"{i*4:04x}: {to_hex(val)}")
        return False

    def do_break(self, arg: str) -> bool:
        addr = parse_number(arg) if arg.isdigit() or arg.startswith("0x") else self.dbg.cpu.labels.get(arg, 0)
        self.dbg.add_breakpoint(addr)
        print(f"Breakpoint set at {addr}")
        return False

    do_b = do_break

    def do_set(self, arg: str) -> bool:
        parts = shlex.split(arg)
        if len(parts) != 2:
            print("usage: set REG VALUE")
            return False
        reg, val = parts
        self.dbg.cpu.regs[reg.upper()] = parse_number(val)
        return False

    def do_quit(self, arg: str) -> bool:
        return True

    do_q = do_quit


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="x86 emulator")
    parser.add_argument("file", help="assembly file to emulate")
    args = parser.parse_args(argv)

    data = load_file(args.file)
    cpu = CPUState()
    cpu.instructions = data["instructions"]
    cpu.labels = data["labels"]

    dbg = Debugger(cpu)
    shell = EmulatorShell(dbg)
    shell.cmdloop()


if __name__ == "__main__":
    main()
