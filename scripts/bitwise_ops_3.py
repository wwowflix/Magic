import numpy as np

i8 = np.int64(1)
u8 = np.uint64(1)

i4 = np.int32(1)
u4 = np.uint32(1)

b_ = np.bool_(1)

b = bool(1)
i = int(1)

AR = np.array([0, 1, 2], dtype=np.int32)
AR.setflags(write=False)

# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}

# E: Any
# E: Any
# E: Any
# E: Any
# E: Any

# E: {int32}
# E: {int32}
# E: {int32}
# E: {int32}
# E: {int32}

# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}

# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}

# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}

# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}
# E: {int64}

# E: {uint64}
# E: {uint64}
# E: {uint64}
# E: {uint64}
# E: {uint64}

# E: Any
# E: Any
# E: Any
# E: Any
# E: Any

# E: {uint32}
# E: {uint32}
# E: {uint32}
# E: {uint32}
# E: {uint32}

# E: numpy.signedinteger[Any]
# E: numpy.signedinteger[Any]
# E: numpy.signedinteger[Any]
# E: numpy.signedinteger[Any]
# E: numpy.signedinteger[Any]

# E: numpy.signedinteger[Any]
# E: numpy.signedinteger[Any]
# E: numpy.signedinteger[Any]
# E: numpy.signedinteger[Any]
# E: numpy.signedinteger[Any]

# E: {uint64}
# E: {uint64}
# E: {uint64}
# E: {uint64}
# E: {uint64}

# E: {uint64}
# E: {uint64}
# E: {uint64}
# E: {uint64}
# E: {uint64}

# E: {int8}
# E: {int8}
# E: numpy.bool_
# E: numpy.bool_
# E: numpy.bool_

# E: Any
# E: Any
# E: Any
# E: Any
# E: Any

# E: {int8}
# E: {int8}
# E: numpy.bool_
# E: numpy.bool_
# E: numpy.bool_

# E: {int_}
# E: {int_}
# E: {int_}
# E: {int_}
# E: {int_}

# E: {int64}
# E: {int32}
# E: {uint64}
# E: {uint32}
# E: numpy.bool_
# E: Any
