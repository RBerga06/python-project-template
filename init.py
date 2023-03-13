#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Substitute variables in the newly-created repository.

To be used until https://github.com/community/community/discussions/5336 is resolved.
"""
from __future__ import annotations
from pathlib import Path
from contextlib import suppress
import shutil
import os

FMT_TOKEN = "${0}$"
FMT_FLAGL = "$IFDEF:{0}$"
FMT_FLAGR = "$ENDIF:{0}$"
FMT_FLAGN = "NO{0}"
DEFAULT_AUTHOR = "RBerga06"
DEFAULT_EMAIL  = "78449715+RBerga06@users.noreply.github.com"


TOKENS = dict[str, tuple[str | None, str]](
    AUTHOR  = (DEFAULT_AUTHOR,        "author username"),
    EMAIL   = (DEFAULT_EMAIL,         "author email"),
    PROJECT = (None,                  "project name"),
    VERSION = ("0.0.1.dev0",          "project version"),
    DESC    = (None,                  "project description"),
    PACKAGE = ("$PROJECT$",           "Python module name"),
    COMMAND = ("$PROJECT$",           "cli command name"),
    REPO    = ("$AUTHOR$/$PROJECT$",  "GitHub repository"),
)

FEATURES = dict[str, tuple[bool | None, str]](
    CLI = (True,    "Include a command-line interface"),
#   GUI = (True,    "Include a graphical user interface"),  # TODO: Implement this
)

SUBS: dict[str, str] = {}
FLAGS: dict[str, bool] = {}


def fix_str(s: str) -> str:
    """Substitute the relevant tokens in the given string."""
    for flag, value in FLAGS.items():
        lflag = FMT_FLAGL.format(flag)
        rflag = FMT_FLAGR.format(flag)
        if lflag in s and rflag in s:
            if flag:
                s = s.replace(lflag, "").replace(rflag, "")
            else:
                s = s.partition(lflag)[0] + s.partition(rflag)[1]
    for token, value in SUBS.items():
        if token in s:
            s = s.replace(token, value)
    return s


def fix_path(src: Path) -> Path:
    """Substitute the relevant tokens in file/dir names."""
    new_name = fix_str(src.name)
    if not new_name:
        if src.is_dir():
            shutil.rmtree(src)
        elif src.is_file():
            os.unlink(src)
        return src
    dst = src.with_name(new_name)
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
    root = fix_path(root)
    if not root.exists():
        return
    if root.is_file():
        fix_contents(root)
    elif root.is_dir():
        for child in root.iterdir():
            fix(child)


def main():
    print("Please activate the relevant features:")
    FLAGS.clear()
    for feature, (default, help) in FEATURES.items():
        FLAGS[feature] = (
            input(f" • {help} [y/n]: ") if default is None else
            input(f" • {help} [{'Y/n' if default else 'y/N'}]: ") or "yn"[default]
        ).lower() in ["y", "yes", "ok", "true"]
        FLAGS[FMT_FLAGN.format(feature)] = not FLAGS[feature]
    print("Please fill in the relevant tokens:")
    SUBS.clear()
    for token, (default, help) in TOKENS.items():
        if default is not None:
            default = fix_str(default)
        SUBS[FMT_TOKEN.format(token)] = (
            input(f" • {help}: ") if default is None else
            input(f" • {help} (default: {default}): ") or default
        )
    print("Applying flags and tokens...", end="", flush=True)
    fix(Path(__file__).parent)
    print("done.")
    print("Removing this file (if possible)...", end="", flush=True)
    with suppress(OSError):
        os.unlink(Path(__file__))
    print("done.")


if __name__ == "__main__":
    main()
