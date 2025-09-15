try:
    with open("missing_input_file.txt", "r") as f:
        data = f.read()
    print("File content:", data)
except FileNotFoundError as e:
    print(" FileNotFoundError triggered:", e)
    raise
