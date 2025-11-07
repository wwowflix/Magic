from typing import Any, Callable
import numpy as np

AR: np.ndarray[Any, Any]
func_float: Callable[[np.floating[Any]], str]
func_int: Callable[[np.integer[Any]], str]

)  # E: TypedDict
reveal_type(
    np.array2string(  # E: str
        AR, formatter={"float_kind": func_float, "int_kind": func_int}
    )
)
)  # E: str
)  # E: str
)  # E: str
)  # E: str

)  # E: contextlib._GeneratorContextManager
with np.printoptions() as dct:
      # E: TypedDict
