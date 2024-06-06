from functools import wraps
import typing
import numpy as np
import inspect


def np_args(func: typing.Callable) -> typing.Callable:
    type_hints = typing.get_type_hints(func)
    converter = {k: np.array for k, v in type_hints.items() if v == np.ndarray}

    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_names = inspect.getfullargspec(func).args
        args_dict = dict(zip(arg_names, args))
        args = [converter.get(k, lambda x: x)(v) for k, v in args_dict.items()]
        kwargs = {k: converter.get(k, lambda x: x)(v) for k, v in kwargs.items()}
        print(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper
