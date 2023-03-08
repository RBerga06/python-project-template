#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Substitute variables in the newly-created repository.

To be used until https://github.com/community/community/discussions/5336 is resolved.
"""
from __future__ import annotations
from typing import NamedTuple
from pathlib import Path
from contextlib import suppress
import shutil
import os


DEFAULT_AUTHOR = "RBerga06"
DEFAULT_EMAIL  = "78449715+RBerga06@users.noreply.github.com"


TOKENS: dict[str, tuple[str | None, str]] = dict(
    AUTHOR  = (DEFAULT_AUTHOR,          "author username"),
    EMAIL   = (DEFAULT_EMAIL,           "author email"),
    NAME    = (None,                    "project name"),
    DESC    = (None,                    "project description"),
    VERSION = ("1.0.0.dev0",            "project version"),
    PYNAME  = ("__NAME__",              "Python module name"),
    CLINAME = ("__NAME__",              "cli command name"),
    REPO    = ("__AUTHOR__/__NAME__",   "GitHub repository"),
)

SUBS: dict[str, str] = {}


def fix_str(s: str) -> str:
    """Substitute the relevant tokens in the given string."""
    for token, value in SUBS.items():
        if token in s:
            s = s.replace(token, value)
    return s


def fix_path(src: Path) -> Path:
    """Substitute the relevant tokens in file/dir names."""
    dst = src.with_name(fix_str(src.name))
    if dst.exists():
        return src
    shutil.move(src, dst)
    return dst


def fix_contents(file: Path) -> None:
    """Fix the given file's contents."""
    with suppress(UnicodeError):
        file.write_text(fix_str(file.read_text("utf-8")), "utf-8")


def fix(root: Path) -> None:
    """Fix the given path (file or dir) [and its subpaths as well]."""
    print(f"Fixing {root}")
    root = fix_path(root)
    print(f"File has been renamed to {root}")
    if root.is_file():
        fix_contents(root)
    elif root.is_dir():
        for child in root.iterdir():
            fix(child)


def main():
    print("Please fill in the relevant tokens:")
    SUBS.clear()
    for token, (help, default) in TOKENS.items():
        default = fix_str(default)
        SUBS[f"__{token}__"] = (
            input(f" • {help}: ") if default is None else
            input(f" • {help} (default: {default}): ") or default
        )
    print("Substituting tokens...", end="", flush=True)
    fix(Path(__file__).parent)
    print("done.")
    print("Removing this file (if possible)...", end="", flush=True)
    with suppress(OSError):
        os.unlink(Path(__file__))
    print("done.")


if __name__ == "__main__":
    main()
