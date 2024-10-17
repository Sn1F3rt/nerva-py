from typing import Literal, NamedTuple

from . import (
    utils as utils,
    daemon as daemon,
    wallet as wallet,
)


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=1, minor=0, micro=0, releaselevel="beta", serial=1
)

del NamedTuple, Literal, VersionInfo
