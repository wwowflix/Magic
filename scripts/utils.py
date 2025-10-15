def to_bool(value):
    """
    Convert common truthy/falsey inputs to bool.
    Accepts: True/False, "true"/"false", "yes"/"no", "1"/"0", 1/0, "y"/"n".
    Anything else raises ValueError (so callers fix their inputs).
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0,1):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true","yes","y","1","on"}:  return True
        if v in {"false","no","n","0","off"}: return False
    raise ValueError(f"Cannot convert to bool: {value!r}")
