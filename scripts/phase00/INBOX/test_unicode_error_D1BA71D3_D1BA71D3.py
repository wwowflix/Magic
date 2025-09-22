text = "This will break:   "

try:
    with open("ascii_only.txt", "w", encoding="ascii") as f:
        f.write(text)
    print("Write success.")
except UnicodeEncodeError as e:
    print(" UnicodeEncodeError triggered:", e)
    raise
