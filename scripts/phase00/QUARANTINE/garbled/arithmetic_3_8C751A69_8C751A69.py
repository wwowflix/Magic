from typing import Any, List
import numpy as np
import numpy.typing as npt

# Can't directly import `np.float128` as it is not available on all platforms
f16: np.floating[npt._128Bit]

c16 = np.complex128()
f8 = np.float64()
i8 = np.int64()
u8 = np.uint64()

c8 = np.complex64()
f4 = np.float32()
i4 = np.int32()
u4 = np.uint32()

dt = np.datetime64(0, "D")
td = np.timedelta64(0, "D")

b_ = np.bool_()

b = bool()
c = complex()
f = float()
i = int()

AR_b: np.ndarray[Any, np.dtype[np.bool_]]
AR_u: np.ndarray[Any, np.dtype[np.uint32]]
AR_i: np.ndarray[Any, np.dtype[np.int64]]
AR_f: np.ndarray[Any, np.dtype[np.float64]]
AR_c: np.ndarray[Any, np.dtype[np.complex128]]
AR_m: np.ndarray[Any, np.dtype[np.timedelta64]]
AR_M: np.ndarray[Any, np.dtype[np.datetime64]]
AR_O: np.ndarray[Any, np.dtype[np.object_]]

AR_LIKE_b: List[bool]
AR_LIKE_u: List[np.uint32]
AR_LIKE_i: List[int]
AR_LIKE_f: List[float]
AR_LIKE_c: List[complex]
AR_LIKE_m: List[np.timedelta64]
AR_LIKE_M: List[np.datetime64]
AR_LIKE_O: List[np.object_]

# Array subtraction

reveal_type(
    AR_b - AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_b - AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_b - AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

reveal_type(
    AR_LIKE_u - AR_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_LIKE_i - AR_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_c - AR_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.datetime64]]
  # E: Any

reveal_type(
    AR_u - AR_LIKE_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_u - AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_u - AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_u - AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

reveal_type(
    AR_LIKE_b - AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_LIKE_u - AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_LIKE_i - AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_c - AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.datetime64]]
  # E: Any

reveal_type(
    AR_i - AR_LIKE_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_i - AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_i - AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_i - AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

reveal_type(
    AR_LIKE_b - AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_LIKE_u - AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_LIKE_i - AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_c - AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.datetime64]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_f - AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_c - AR_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

reveal_type(
    AR_c - AR_LIKE_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_c - AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_c - AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_c - AR_LIKE_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_c - AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

reveal_type(
    AR_LIKE_b - AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_LIKE_u - AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_LIKE_i - AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_LIKE_f - AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_LIKE_c - AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.datetime64]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[numpy.datetime64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.datetime64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.datetime64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.datetime64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any

  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any

# Array floor division

  # E: numpy.ndarray[Any, numpy.dtype[{int8}]]
reveal_type(
    AR_b // AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_b // AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_b // AR_LIKE_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_b // AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[{int8}]]
reveal_type(
    AR_LIKE_u // AR_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_LIKE_i // AR_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_LIKE_f // AR_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_c // AR_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

reveal_type(
    AR_u // AR_LIKE_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_u // AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_u // AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_u // AR_LIKE_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_u // AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

reveal_type(
    AR_LIKE_b // AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_LIKE_u // AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.unsignedinteger[Any]]]
reveal_type(
    AR_LIKE_i // AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_LIKE_f // AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_c // AR_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

reveal_type(
    AR_i // AR_LIKE_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_i // AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_i // AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_i // AR_LIKE_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_i // AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

reveal_type(
    AR_LIKE_b // AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_LIKE_u // AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_LIKE_i // AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.signedinteger[Any]]]
reveal_type(
    AR_LIKE_f // AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_c // AR_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

reveal_type(
    AR_f // AR_LIKE_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_f // AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_f // AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_f // AR_LIKE_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_f // AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

reveal_type(
    AR_LIKE_b // AR_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_u // AR_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_i // AR_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_f // AR_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.floating[Any]]]
reveal_type(
    AR_LIKE_c // AR_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: Any

reveal_type(
    AR_c // AR_LIKE_b
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_c // AR_LIKE_u
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_c // AR_LIKE_i
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_c // AR_LIKE_f
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_c // AR_LIKE_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

reveal_type(
    AR_LIKE_b // AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_LIKE_u // AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_LIKE_i // AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_LIKE_f // AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
reveal_type(
    AR_LIKE_c // AR_c
)  # E: numpy.ndarray[Any, numpy.dtype[numpy.complexfloating[Any, Any]]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[numpy.timedelta64]]
  # E: numpy.ndarray[Any, numpy.dtype[{int64}]]
  # E: Any

  # E: numpy.ndarray[Any, numpy.dtype[{int64}]]
  # E: Any

  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any

  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any
  # E: Any

# unary ops

  # E: {float128}
  # E: {complex128}
  # E: {complex64}
  # E: {float64}
  # E: {float32}
  # E: {int64}
  # E: {int32}
  # E: {uint64}
  # E: {uint32}
  # E: numpy.timedelta64
  # E: Any

  # E: {float128}
  # E: {complex128}
  # E: {complex64}
  # E: {float64}
  # E: {float32}
  # E: {int64}
  # E: {int32}
  # E: {uint64}
  # E: {uint32}
  # E: numpy.timedelta64
  # E: Any

)  # E: {float128}
)  # E: {float64}
)  # E: {float32}
)  # E: {float64}
)  # E: {float32}
)  # E: {int64}
)  # E: {int32}
)  # E: {uint64}
)  # E: {uint32}
)  # E: numpy.timedelta64
)  # E: numpy.bool_
)  # E: Any

# Time structures

  # E: numpy.datetime64
  # E: numpy.datetime64
  # E: numpy.datetime64
  # E: numpy.datetime64
  # E: numpy.timedelta64
  # E: numpy.datetime64
  # E: numpy.datetime64
  # E: numpy.datetime64

  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: numpy.timedelta64
  # E: {float64}
  # E: {int64}

# boolean

  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float128}
  # E: {float64}
  # E: {float32}
  # E: {complex128}
  # E: {complex128}
  # E: {complex64}

  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float128}
  # E: {float64}
  # E: {float32}
  # E: {complex128}
  # E: {complex128}
  # E: {complex64}

# Complex

  # E: {complex256}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: Any

  # E: {complex256}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: Any

  # E: {complex256}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex64}
  # E: {complex64}
  # E: {complex64}
  # E: {complex64}
  # E: {complex64}
  # E: {complex128}
  # E: {complex128}
  # E: numpy.complexfloating[{_NBitInt}, {_NBitInt}]
  # E: Any

  # E: {complex256}
  # E: {complex128}
  # E: {complex128}
  # E: {complex128}
  # E: {complex64}
  # E: {complex64}
  # E: {complex64}
  # E: {complex64}
  # E: {complex64}
  # E: {complex128}
  # E: {complex128}
  # E: numpy.complexfloating[{_NBitInt}, {_NBitInt}]
  # E: Any

# Float

  # E: {float128}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {complex128}
  # E: {float64}
  # E: {float64}
  # E: Any

  # E: {float128}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {float64}
  # E: {complex128}
  # E: {float64}
  # E: {float64}
  # E: Any

  # E: {float128}
  # E: {float64}
  # E: {float64}
  # E: {float32}
  # E: {float32}
  # E: {float32}
  # E: {float32}
  # E: {complex128}
  # E: {float64}
  # E: numpy.floating[{_NBitInt}]
  # E: Any

  # E: {float128}
  # E: {float64}
  # E: {float64}
  # E: {float32}
  # E: {float32}
  # E: {float32}
  # E: {float32}
  # E: {complex128}
  # E: {float64}
  # E: numpy.floating[{_NBitInt}]
  # E: Any

# Int

  # E: {int64}
  # E: Any
  # E: {int64}
  # E: Any
  # E: {int64}
  # E: {int64}
  # E: {complex128}
  # E: {float64}
  # E: {int64}
  # E: Any

  # E: {uint64}
  # E: Any
  # E: {uint64}
  # E: {uint64}
  # E: {uint64}
  # E: {complex128}
  # E: {float64}
  # E: Any
  # E: Any

  # E: {int64}
  # E: Any
  # E: {int64}
  # E: Any
  # E: {int64}
  # E: {int64}
  # E: {complex128}
  # E: {float64}
  # E: {int64}
  # E: Any

  # E: {uint64}
  # E: Any
  # E: {uint64}
  # E: {uint64}
  # E: {uint64}
  # E: {complex128}
  # E: {float64}
  # E: Any
  # E: Any

  # E: {int64}
  # E: {int32}
  # E: {int_}
  # E: {int32}
  # E: {int32}
  # E: Any

  # E: Any
  # E: Any
  # E: {uint64}
  # E: {uint32}
  # E: Any
  # E: {uint32}
  # E: {uint32}
  # E: Any

  # E: {int64}
  # E: {int32}
  # E: {int_}
  # E: {int32}
  # E: {int32}
  # E: Any

  # E: Any
  # E: Any
  # E: {uint64}
  # E: {uint32}
  # E: {uint32}
  # E: {uint32}
  # E: Any
  # E: Any
