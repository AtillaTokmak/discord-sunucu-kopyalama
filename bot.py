import discord
import asyncio
from discord.ext import commands
import os

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)

    async def on_ready(self):
        print('Bot online')

bot = Bot()

# load cog
@bot.command(name="load_cog")
@commands.has_permissions(administrator=True)
async def load_cog(ctx, string):
    string = 'cogs.' + string
    try:
        await bot.load_extension(string)
        print(f'Loaded extension "{string}"')
        await ctx.send(f'Loaded extension "{string}"')
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to load extension "{string}"\n{exc}')
        await ctx.send(f'Failed to load extension "{string}"')

# unload cog
@bot.command(name="unload_cog")
@commands.has_permissions(administrator=True)
async def unload_cog(ctx, string):
    string = 'cogs.' + string
    try:
        await bot.unload_extension(string)
        print(f'Unloaded extension "{string}"')
        await ctx.send(f'Unloaded extension "{string}"')
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to unload extension "{string}"\n{exc}')
        await ctx.send(f'Failed to unload extension "{string}"')

# reload cog
@bot.command(name="reload_cog")
@commands.has_permissions(administrator=True)
async def reload_cog(ctx, string):
    string = 'cogs.' + string
    try:
        await bot.unload_extension(string)
        print(f'Unloaded extension "{string}"')
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to unload extension "{string}"\n{exc}')
    try:
        await bot.load_extension(string)
        print(f'Loaded extension "{string}"')
        await ctx.send(f'Reloaded extension "{string}"')
    except Exception as e:
        exc = f'{type(e).__name__}: {e}'
        print(f'Failed to load extension "{string}"\n{exc}')
        await ctx.send(f'Failed to load extension "{string}"')

async def load_extensions():
    for rootfile in os.listdir("./cogs"):
        if rootfile.endswith('.py'):
            await bot.load_extension(f"cogs.{rootfile[:-3]}")
            print(f"cogs.{rootfile[:-3]}")
        else:
            for subfile in os.listdir(f"cogs/{rootfile}"):
                if subfile.endswith("cog.py"):
                    await bot.load_extension(f"cogs.{rootfile}.{subfile[:-3]}")
                    print(f"cogs.{rootfile}.{subfile[:-3]}")

async def main():
    await load_extensions()
    try:
        await bot.start(input('input token: '))
    except discord.errors.LoginFailure:
        print('[Error] Failed to run bot. Check your token')
        input("Press enter to close the program... ")

if __name__ == "__main__":
    asyncio.run(main())
