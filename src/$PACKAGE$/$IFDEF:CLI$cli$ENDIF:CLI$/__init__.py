#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional
import typer
from ..__about__ import *


app = typer.Typer(
    name=__command__,
    context_settings=dict(
        help_option_names=['-h', '--help']
    ),
    invoke_without_command=True,
)


def version(version: bool) -> None:
    if version:
        typer.echo(f"{__command__}: {__version__}")
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
