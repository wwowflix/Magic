try:
    import non_existent_package_123

    print("Module imported successfully.")
except ImportError as e:
    print(" ImportError triggered:", e)
    raise
