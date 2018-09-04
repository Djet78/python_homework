import os
from contextlib import contextmanager

# ------------------- Task 1 ----------------------


def generate_items_from_nested(nested_iterable):
    for elem in nested_iterable:
        check_nest = getattr(elem, "__iter__", False)
        if check_nest:
            for nest in generate_items_from_nested(elem):
                yield nest
        else:
            yield elem

# ------------------- Task 2 ----------------------


class ChDirManager:
    """
    Context manager which changes working directory.

    :param dir_path: Full path to other directory.
    :param exc_to_suppress: Takes Exception which you want to suppress, 'None' by default.
    :param get_back: Change directory back. 'True' by default.
    """

    def __init__(self, dir_path, exc_to_suppress=None, get_back=True):
        self.dir_path = dir_path
        self.suppress = exc_to_suppress
        self.get_back = get_back
        self.prev_dir = os.getcwd()

    def __enter__(self):
        os.chdir(self.dir_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.get_back:
            os.chdir(self.prev_dir)
        print(exc_type)
        return exc_type is not None and issubclass(exc_type, self.suppress)

# ------------------- Task 3 ----------------------


@contextmanager
def ch_dir_manager(dir_path, exc_to_suppress=None, get_back=True):
    """ Is same as a class above"""
    prev_dir = os.getcwd()
    try:
        os.chdir(dir_path)
        yield
    except exc_to_suppress:
        print("Exception was suppressed!")
    finally:
        if get_back:
            os.chdir(prev_dir)
