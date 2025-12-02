def make_path_posix(path):
    if isinstance(path, str):
        return path.replace("\\", "/")
    return path
