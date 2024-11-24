def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        for arg, arg_type in zip(args, annotations.values()):
            if not isinstance(arg, arg_type):
                raise TypeError(f"Expected {arg_type}, got {type(arg)}")
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_int(a: int, b: int) -> int:
    return a + int(b)


@strict
def sum_intchar_str(a: int, b: str):
    return a + int(b)


@strict
def sum_bool(a: bool, b: bool):
    return a + b


@strict
def sum_bool_int(a: bool, b: bool):
    return a + b


@strict
def concat(a: str, b: str):
    return str(a) + str(b)


if __name__ == '__main__':
    print(sum_int(1, 2))
    print(sum_intchar_str(1, '2'))
    print(sum_bool(True, False))
    print(sum_bool_int(True, 1))
    print(concat('a', 'b'))
