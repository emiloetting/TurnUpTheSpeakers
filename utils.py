from pathlib import Path
from warnings import warn


def check_dtype(value, target_dtype, name):
    """Validates that `value` is an instance of `target_dtype`.

    Args:
        value: Value to validate.
        target_dtype (type|tuple[type]): Expected type, or tuple of acceptable types.
        name (str): Name of the value, used in error messages.
    Returns:
        value: The validated value, unchanged.
    """
    dtypes = target_dtype if isinstance(target_dtype, tuple) else (target_dtype,)   # always make tuple

    # Catch boolean-int relation and not let int pass for bool / other way around
    if isinstance(value, bool) and bool not in dtypes:
        raise TypeError(f"Config <{name}> must be of type <{target_dtype}>, but is {type(value)}.")

    if not isinstance(value, target_dtype):
        raise TypeError(f"Config <{name}> must be of type <{target_dtype}>, but is {type(value)}.")
    return value


def validate_float_arg(value, name: str, min_value: float | None = None, max_value: float | None = None) -> float:
    """Validates that `value` represents a real number within an optional range.

    Args:
        value: Value to validate (already a `float`/`int`, or castable to one, e.g. "1.5" or 2).
        name (str): Name of the argument, used in error messages.
        min_value (float|None): Optional inclusive lower bound.
        max_value (float|None): Optional inclusive upper bound.

    Returns:
        float: The validated value as a real `float`.
    """
    if not isinstance(value, float):
        try:
            value = float(value)
        except Exception:
            raise ValueError(f"Argument <{name}> must be of type <float>, but is {type(value)}: <{value}>!")

    if min_value is not None and value < min_value:
        raise ValueError(f"Argument <{name}> must be >= {min_value}, but is <{value}>!")
    if max_value is not None and value > max_value:
        raise ValueError(f"Argument <{name}> must be <= {max_value}, but is <{value}>!")

    return value


def validate_int_arg(value, name: str, min_value: int | None = None, max_value: int | None = None) -> int:
    """Validates that `value` represents a whole number within an optional range.

    Args:
        value: Value to validate (already an `int`, or castable to one without loss, e.g. "8080" or 8080.0).
        name (str): Name of the argument, used in error messages.
        min_value (int|None): Optional inclusive lower bound.
        max_value (int|None): Optional inclusive upper bound.

    Returns:
        int: The validated value as a real `int`.
    """
    # Although bool is subclass of int, do not let silently pass
    if isinstance(value, bool):
        raise ValueError(f"Argument <{name}> must be of type <int>, but is {type(value)}: <{value}>!")

    if not isinstance(value, int):
        try:
            inted = int(value)
        except Exception:
            raise ValueError(f"Argument <{name}> must be of type <int>, but is {type(value)}: <{value}>!")
        if inted != float(value):
            raise ValueError(f"Argument <{name}> must be a whole number, but is <{value}> (would truncate to <{inted}>)!")
        value = inted

    if min_value is not None and value < min_value:
        raise ValueError(f"Argument <{name}> must be >= {min_value}, but is <{value}>!")
    if max_value is not None and value > max_value:
        raise ValueError(f"Argument <{name}> must be <= {max_value}, but is <{value}>!")

    return value


def validate_path_arg(path, name: str, kind: str = "file", must_exist: bool = True, warn_on_missing: bool = False) -> Path:
    """Validates that `value` is a filesystem path pointing to a file or directory.

    Args:
        path: Path to validate (`str` or `Path`).
        name (str): Name of the argument, used in error messages.
        kind (str): Either "file" or "dir" — what the path must point to.
        must_exist (bool): If True, the path must already exist as `kind`.
        warn_on_missing (bool): Whether or not to raise a warning if `must_exist`is `False` and `path` does indeed not exist.
    Returns:
        Path: The validated path as a `Path` object.
    """
    # Validate inputs
    if not isinstance(kind, str):
        raise TypeError(f"Argument <kind> must be of type <str>, but is {type(kind)}.")
    if kind.lower().strip() not in ("file", "dir"):
        raise ValueError(f"Argument <kind> must be 'file' or 'dir', but is <{kind}>.")
    kind = kind.lower().strip() # ensure to work with what has been checked

    if not isinstance(path, (str, Path)):
        raise ValueError(f"Argument <{name}> must be of type <str> or <Path>, but is {type(path)}.")

    if not isinstance(name, str):
        raise TypeError(f"Argument <name> must be of type <str>, but is {type(name)}.")

    if not isinstance(must_exist, bool):
        raise TypeError(f"Argument <must_exist> must be of type <bool>, but is {type(must_exist)}.")

    if not isinstance(warn_on_missing, bool):
        raise TypeError(f"Argument <warn_on_missing> must be of type <bool>, but is {type(must_exist)}.")
    path = Path(path)

    if must_exist:
        if kind == "file" and not path.is_file():
            raise ValueError(f"Argument <{name}> must point to an existing file, but <{path}> does not.")
        if kind == "dir" and not path.is_dir():
            raise ValueError(f"Argument <{name}> must point to an existing directory, but <{path}> is not.")
    else:
        if not path.exists() and warn_on_missing:
            warn(f"Argument <{name}> does not yet exist!")
    return path


def validate_ip(host_ip: str, host_port: int) -> tuple[str, int]:
    """Validates host_ip/host_port and returns them normalized (host_port as a real <int>)."""
    if not isinstance(host_ip, str):    # check dtype
        raise TypeError(f"Argument <host_ip> must be of type <str>, but is {type(host_ip)}")

    # Inspect IPv4 format
    host_ip = host_ip.strip()
    splits = host_ip.split(".")     # check for len of list

    if not len(splits) == 4:
        raise ValueError(f"Invalid IPv4 passed for argument <host_ip>: <{host_ip}>")

    for subn in splits:
        # If type conversion fails IP-adress is invalid
        try:
            inted = int(subn)
        except Exception:
            raise ValueError(f"Argument <host_ip> must be a valid IPv4 adress (containing 4 integers split on '.') but is <{host_ip}>!")

        # Inspect individual components of
        if not 0 <= inted <= 255:
            raise ValueError(f"Argument <host_ip> contains invalid parts. All adress-components must be integers within [0,255]. Given <host_ip> was <{host_ip}>")

    # Inspect port-argument
    host_port = validate_int_arg(host_port, "host_port", min_value=0, max_value=65535)

    return host_ip, host_port