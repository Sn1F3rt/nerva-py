from __future__ import annotations

import random
import string


def generate_payment_id() -> str:
    """
    Generate a random payment ID for transactions.

    Returns
    -------
    str
        A random 64-bit payment ID.

    """
    return "".join(random.choices(string.hexdigits, k=64)).lower()


def calculate_seconds_from_time_string(time_string: str) -> int:
    """
    Calculate seconds from time string.

    Parameters
    ----------
    time_string : str
        The time string to convert to seconds.

    Returns
    -------
    int
        The number of seconds in the time string.

    """
    time: list = time_string.split(" ")

    seconds: int = 0

    t: str
    for t in time:
        if t.endswith("s"):
            seconds += int(t[:-1])

        if t.endswith("m"):
            seconds += int(t[:-1]) * 60

        if t.endswith("h"):
            seconds += int(t[:-1]) * 3600

        if t.endswith("d"):
            seconds += int(t[:-1]) * 86400

    return seconds
