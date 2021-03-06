from __future__ import annotations

import functools
import io
import os
import subprocess  # nosec
import sys
from concurrent.futures import ThreadPoolExecutor

import discord
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS


class Runner(commands.Cog):
    """
    Look, it works. Be careful when using this.
    """

    __version__ = "323.0.1"

    def format_help_for_context(self, ctx):
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\nCog Version: {self.__version__}"

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.executor = ThreadPoolExecutor()

    def cog_unload(self):
        self.executor.shutdown(wait=False)

    async def _run(self, command):
        env = os.environ.copy()
        if hasattr(sys, "real_prefix") or sys.base_prefix != sys.prefix:
            # os.path.sep - this is folder separator, i.e. `\` on win or `/` on unix
            # os.pathsep - this is paths separator in PATH, i.e. `;` on win or `:` on unix
            # a wonderful idea to call them almost the same >.<
            if sys.platform == "win32":
                binfolder = f"{sys.prefix}{os.path.sep}Scripts"
                env["PATH"] = f"{binfolder}{os.pathsep}{env['PATH']}"
            else:
                binfolder = f"{sys.prefix}{os.path.sep}bin"
                env["PATH"] = f"{binfolder}{os.pathsep}{env['PATH']}"
        return (
            await self.bot.loop.run_in_executor(
                self.executor,
                functools.partial(
                    subprocess.run,
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True,  # nosec
                    env=env,
                ),
            )
        ).stdout

    @checks.is_owner()
    @commands.command()
    async def shell(self, ctx: commands.Context, *, command: str):
        """
        Runs a command.
        """
        async with ctx.typing():
            result = await self._run(command)
            fp = io.BytesIO(result)
            fp.seek(0)
        await ctx.send(files=[discord.File(fp, filename=f"{ctx.message.id}.log")])

    @checks.is_owner()
    @commands.command()
    async def shelld(self, ctx: commands.Context, *, command: str):
        """
        Runs a command, output in chat.
        """
        async with ctx.typing():
            result = (await self._run(command)).decode()

        if not result:
            return await ctx.tick()

        rpages = [box(p) for p in pagify(result, shorten_by=(len(command) + 100))]
        plen = len(rpages)
        pages = [
            f"Page {index} / {plen} of output for\n{box(command)}\n{rpage}"
            for index, rpage in enumerate(rpages, 1)
        ]
        await menu(ctx, pages, DEFAULT_CONTROLS)

    @checks.is_owner()
    @commands.command()
    async def killshells(self, ctx: commands.Context):
        """
        kills the shells
        """
        self.executor.shutdown(wait=False)
        self.executor = ThreadPoolExecutor()
        await ctx.tick()
