"""Load assembly files into instructions."""

from __future__ import annotations

import re
from typing import Dict, List


INSTRUCTION_RE = re.compile(r"^\s*(?:(?P<label>\w+):)?\s*(?P<op>\w+)?\s*(?P<args>.*)?$")


def load_file(filename: str) -> Dict[str, List[Dict]]:
    instructions: List[Dict] = []
    labels: Dict[str, int] = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.split(";", 1)[0].rstrip()
            if not line:
                continue
            m = INSTRUCTION_RE.match(line)
            if not m:
                continue
            label, op, args = m.group("label", "op", "args")
            if label is not None:
                labels[label] = len(instructions)
            if op:
                operands = [a.strip() for a in args.split(',')] if args else []
                instructions.append({"op": op.upper(), "args": operands, "text": line})
    return {"instructions": instructions, "labels": labels}
