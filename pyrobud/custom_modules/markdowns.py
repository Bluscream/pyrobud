"""
A pyrobud module for easier markdowns.
Author : Ojas Sinha<sinhaojas67@gmail.com>
"""

from pyrobud import command, module

class Markdowns(module.Module):
    name: str="Markdowns"
    disabled: bool= False

    @command.desc("Bold")
    @command.alias("b")
    async def cmd_bold(self, ctx: command.Context) -> str:
        if not ctx.input:
            return "**Enter the text**"
        text = ctx.input
        return "**" + text + "**"

    @command.desc("Italics")
    @command.alias("it")
    async def cmd_italics(self, ctx: command.Context) -> str:
        if not ctx.input:
            return "__Enter the text__"
        text = ctx.input
        return "__" + text + "__"

    @command.desc("Monospace")
    @command.alias("mo")
    async def cmd_mono(self, ctx: command.Context) -> str:
        if not ctx.input:
            return "`Enter the text`"
        text = ctx.input
        return "'" + text + "'"
