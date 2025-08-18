data = "Hello World â€“ This contains a non-ASCII dash"
with open("outputs/test_unicode.log", "w", encoding="ascii") as f:
    f.write(data)
