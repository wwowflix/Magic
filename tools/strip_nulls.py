import pathlib

for rel in pathlib.Path("outputs/reports/_fail_paths.txt").read_text().splitlines():
    p = pathlib.Path(rel)
    if p.is_file():
        b = p.read_bytes()
        if b.find(b"\x00") >= 0:
            p.write_bytes(b.replace(b"\x00", b""))
            print("Stripped nulls:", p)
