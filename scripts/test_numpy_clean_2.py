import numpy as np
import pandas as pd

print("✅ Numpy version:", np.__version__)
print("✅ Pandas version:", pd.__version__)
print("✅ randbits test:", np.random.default_rng().integers(0, 100))
