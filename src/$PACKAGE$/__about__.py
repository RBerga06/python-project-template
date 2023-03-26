#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""$DESC$"""
from __future__ import annotations
from typing import TYPE_CHECKING

# Project information
__project__ = "$PROJECT$"  # Distribution name#$IFDEF:CLI$#
__command__ = "$COMMAND$"  # CLI main command name#$ENDIF:CLI$#
__version__ = "$VERSION$"  # managed by `hatch`


if TYPE_CHECKING:
    from importlib.metadata import Distribution
    from typing import TypeVar, ContextManager
    from pathlib import Path
    _T = TypeVar("_T")
    def cache(f: _T) -> _T: ...
else:
    from functools import cache


@cache
def __rpath__(child: str) -> ContextManager[Path]:
    """Returns the `Path` of `child` in this distribution."""
    from importlib.resources import files, as_file
    return as_file(files(__package__) / child)


@cache
def __dist__() -> Distribution:
    """Returns `$PROJECT$`'s :class:`importlib.metadata.Distribution` object."""
    from importlib.metadata import distribution
    return distribution("$PROJECT$")


__all__ = [
    "__project__",
    "__command__",
    "__version__",
    "__rpath__",
    "__dist__",
]
