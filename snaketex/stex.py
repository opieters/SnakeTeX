#!/usr/bin/env python3

import click
import snaketex.core as stex

@click.group()
@click.option('--config', default="config.yml", help="Configuration file.")
@click.option('--debug', default=False, help="Debug mode.")
@click.pass_context
def cli(ctx, config, debug):
    """SnakTeX command line interface - write LaTeX faster through templating."""
    ctx.obj['config'] = config
    ctx.obj['engine'] = stex.SnakeTeX(config_file=config, debug=debug)

@cli.command()
@click.pass_context
def build(ctx, exclude_recipe):
    click.echo("Building output file.")
    ctx.obj['engine'].build()

@cli.command()
@click.option('--update_time', default=1, type=click.BOOL)
@click.argument('exclude_recipe', nargs=-1)
@click.pass_context
def compile(cts,update_time, exclude_recipe):
    cts.obj['engine'].compile(bool(update_time))

@cli.command()
@click.pass_context
def clean(cts,update_time):
    cts.obj['engine'].clean()

def main():
    cli(obj={})
