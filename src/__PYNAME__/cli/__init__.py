#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional
import typer
from ..__about__ import *


NAME = __dist__.entry_points.select(module=__name__, attr="app")[0].name


app = typer.Typer(
    name=NAME,
    context_settings=dict(
        help_option_names=['-h', '--help']
    ),
    invoke_without_command=True,
)


def version(version: bool) -> None:
    if version:
        typer.echo(f"{NAME}: {__version__}")
        raise typer.Exit()


@app.command()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-V",
        callback=version, is_eager=True,
        help="Show program version.",
    )
):
    typer.echo("Hello, World!")
