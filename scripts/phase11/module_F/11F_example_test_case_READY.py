# [PASS] Example Test Case for Phase 11F
def validate_ai_behavior(input_data):
    if input_data == "bias":
        return "flagged"
    return "clean"

# Test
if __name__ == "__main__":
    assert validate_ai_behavior("bias") == "flagged"
    assert validate_ai_behavior("neutral") == "clean"
    print("[PASS] All example tests passed.")

