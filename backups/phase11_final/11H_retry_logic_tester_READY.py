import time
import random

for i in range(5):
    if random.random() < 0.6:
        print(f"Try {i+1} failed.")
        time.sleep(0.5)
    else:
        print(f"Success on try {i+1}")
        break
