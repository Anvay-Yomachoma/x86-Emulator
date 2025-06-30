"""Simple calling convention stubs."""

from __future__ import annotations

from typing import Callable, Dict

from .core import CPUState


EXTERNAL_CALLS: Dict[str, Callable[[CPUState], None]] = {}


def register_call(name: str, func: Callable[[CPUState], None]) -> None:
    EXTERNAL_CALLS[name.lower()] = func


def handle_call(cpu: CPUState, name: str) -> None:
    func = EXTERNAL_CALLS.get(name.lower())
    if func:
        func(cpu)
    else:
        print(f"[warn] no handler for external function '{name}'")


def printf_stub(cpu: CPUState) -> None:
    print("[stub] printf called")
    cpu.regs["EAX"] = 0


register_call("printf", printf_stub)
