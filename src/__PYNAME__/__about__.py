#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__DESC__"""
from importlib.metadata import distribution as _get_dist

__dist__ = _get_dist("__NAME__")
__version__ = __dist__.version
__author__ = __dist__.metadata["Author"]


__all__ = [
    "__dist__",
    "__version__",
    "__author__",
]
