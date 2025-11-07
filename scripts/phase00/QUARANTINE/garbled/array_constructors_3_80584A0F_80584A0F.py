from typing import List, Any
import numpy as np

class SubClass(np.ndarray): ...

i8: np.int64

A: np.ndarray
B: SubClass
C: List[int]

def func(i: int, j: int, **kwargs: Any) -> SubClass: ...

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: SubClass
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: SubClass
)  # E: SubClass
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: SubClass
)  # E: SubClass
)  # E: SubClass
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: Tuple[numpy.ndarray[Any, Any], Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: SubClass
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: SubClass
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: SubClass
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: SubClass
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: tuple[numpy.ndarray[Any, Any]]

))  # E: SubClass

)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: list[numpy.ndarray[Any, Any]]
)  # E: list[numpy.ndarray[Any, Any]]
)  # E: list[numpy.ndarray[Any, Any]]

)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
)  # E: SubClass

)  # E: numpy.ndarray[Any, Any]
)  # E: numpy.ndarray[Any, Any]
