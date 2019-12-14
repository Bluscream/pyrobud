import logging
import os
import pkgutil
from importlib import reload as _importlib_reload
from typing import Sequence

log = logging.getLogger("metamod")


def reload() -> None:
    log.info("Reloading module classes")
    for sym in __all__:
        module = globals()[sym]
        _importlib_reload(module)


__all__: Sequence[str] = list(info.name for info in pkgutil.iter_modules([os.path.dirname(__file__)]))

from . import *


try:
    _reload_flag: bool

    # noinspection PyUnboundLocalVariable
    if _reload_flag:
        # Module has been reloaded, reload our submodules
        reload()
except NameError:
    _reload_flag = True
