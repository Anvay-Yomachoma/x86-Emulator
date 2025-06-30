from emulator.loader import load_file


def test_load_file(tmp_path):
    asm = tmp_path / "test.asm"
    asm.write_text("""\nstart: MOV EAX, 1\n""")
    data = load_file(str(asm))
    assert data["labels"]["start"] == 0
    assert data["instructions"][0]["op"] == "MOV"
