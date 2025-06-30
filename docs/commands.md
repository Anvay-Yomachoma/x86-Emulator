# Emulator CLI Commands

Use `emu-cli <file>` to start an interactive session.

Commands:

- `n` or `next`: execute the next instruction
- `c` or `cont`: continue execution until the next breakpoint or end
- `b <addr|label>`: set a breakpoint
- `regs`: display registers
- `stack [n]`: display `n` words from the stack (default 4)
- `set <reg> <value>`: set register `reg` to `value`
- `quit` or `q`: exit the emulator

Invoke `emu-cli --help` for command-line options.
