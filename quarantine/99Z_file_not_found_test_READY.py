import sys
with open('non_existent_input.txt', 'r') as f:
    data = f.read()
print("This should fail because the file does not exist.")
