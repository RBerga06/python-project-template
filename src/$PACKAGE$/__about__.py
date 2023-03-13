#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marks calculator"""
from __future__ import annotations
from typing import TYPE_CHECKING

# Project information
__project__ = "$PROJECT$"  # Distribution name#__IFDEF:CLI__#
__command__ = "$COMMAND$"  # CLI main command name#__ENDIF:CLI__#
__version__ = "$VERSION$"  # managed by `hatch`


if TYPE_CHECKING:
    from importlib.metadata import Distribution
    from typing import TypeVar
    _T = TypeVar("_T")
    def cache(f: _T) -> _T: ...
else:
    from functools import cache


@cache
def __dist__() -> Distribution:
    """Cached `importlib.metadata.distribution("$PROJECT$")`."""
    from importlib.metadata import distribution
    return distribution("marks-calc")


__all__ = [
    "__project__",
    "__command__",
    "__version__",
    "__dist__",
]
