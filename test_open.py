file_path = r"C:\temp\magic_file.csv"

try:
    with open(file_path, "r") as f:
        print("File opened successfully!")
        print(f.readline())
except Exception as e:
    print(f"Failed to open file: {e}")
