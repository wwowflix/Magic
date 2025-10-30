from typing import Any
import numpy as np

AR_i8: np.ndarray[Any, np.dtype[np.int64]]
ar_iter = np.lib.Arrayterator(AR_i8)

  # E: numpy.ndarray[Any, numpy.dtype[{int64}]]
  # E: Union[None, builtins.int]
  # E: builtins.list[builtins.int]
  # E: builtins.list[builtins.int]
  # E: builtins.list[builtins.int]
  # E: builtins.tuple[builtins.int]
  # E: typing.Generator[{int64}, None, None]

)  # E: numpy.ndarray[Any, numpy.dtype[{int64}]]

for i in ar_iter:
      # E: numpy.ndarray[Any, numpy.dtype[{int64}]]

reveal_type(
    ar_iter[0]
)  # E: numpy.lib.arrayterator.Arrayterator[Any, numpy.dtype[{int64}]]
reveal_type(
    ar_iter[...]
)  # E: numpy.lib.arrayterator.Arrayterator[Any, numpy.dtype[{int64}]]
reveal_type(
    ar_iter[:]
)  # E: numpy.lib.arrayterator.Arrayterator[Any, numpy.dtype[{int64}]]
reveal_type(
    ar_iter[0, 0, 0]
)  # E: numpy.lib.arrayterator.Arrayterator[Any, numpy.dtype[{int64}]]
reveal_type(
    ar_iter[..., 0, :]
)  # E: numpy.lib.arrayterator.Arrayterator[Any, numpy.dtype[{int64}]]
