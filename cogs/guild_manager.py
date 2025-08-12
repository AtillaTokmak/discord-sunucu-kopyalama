import discord
from discord.ext import commands
import asyncio
import json
import os

class ServerClone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def clear_channels(self, ctx):
        for ch in ctx.guild.channels:
            try:
                await ch.delete(reason="Server clone cleanup")
            except:
                pass

    async def clear_roles(self, ctx):
        for role in ctx.guild.roles:
            if role.is_default() or role.managed:
                continue
            try:
                await role.delete(reason="Server clone cleanup")
            except:
                pass

    async def fetch_overwrites(self, element):
        overwrites = {}
        for target, perms in element.overwrites.items():
            if getattr(target, "managed", False):
                continue
            overwrites[target.name] = dict(perms)
        return overwrites

    async def gather_channels(self, ctx):
        data = {}
        for ch in ctx.guild.channels:
            if ch.type == discord.ChannelType.category:
                continue
            overwrites = await self.fetch_overwrites(ch)
            data[ch.name] = {
                "type": ch.type.name,
                "position": ch.position,
                "category": ch.category.name if ch.category else None,
                "nsfw": getattr(ch, "nsfw", False),
                "permissions_synced": ch.permissions_synced,
                "overwrites": None if ch.permissions_synced else overwrites
            }
        return data

    async def gather_categories(self, ctx):
        data = {}
        for cat in ctx.guild.categories:
            overwrites = await self.fetch_overwrites(cat)
            data[cat.name] = {
                "position": cat.position,
                "overwrites": overwrites
            }
        return data

    async def gather_roles(self, ctx):
        data = {}
        for role in ctx.guild.roles:
            if role.managed:
                continue
            data[role.name] = {
                "position": role.position,
                "colour": {
                    "r": role.colour.r,
                    "g": role.colour.g,
                    "b": role.colour.b
                },
                "mentionable": role.mentionable,
                "permissions": dict(role.permissions)
            }
        return data

    async def recreate_roles(self, ctx, guild_data):
        mapping = {}
        for name, info in guild_data['roles'].items():
            colour = discord.Colour.from_rgb(**info['colour'])
            if name == '@everyone':
                await ctx.guild.default_role.edit(
                    mentionable=info['mentionable'],
                    colour=colour
                )
                mapping[name] = ctx.guild.default_role
                continue
            try:
                new_role = await ctx.guild.create_role(
                    name=name,
                    mentionable=info['mentionable'],
                    colour=colour
                )
                mapping[name] = new_role
            except:
                pass
        return mapping

    async def recreate_channels(self, ctx, guild_data, roles_map):
        categories_map = {}
        for cat_name, cat_info in guild_data['categories'].items():
            overwrites = {
                roles_map.get(role): discord.PermissionOverwrite(**perms)
                for role, perms in cat_info['overwrites'].items()
                if role in roles_map
            }
            try:
                category = await ctx.guild.create_category(
                    name=cat_name,
                    position=cat_info.get("position"),
                    overwrites=overwrites
                )
                categories_map[cat_name] = category
            except:
                pass

        for ch_name, ch_info in guild_data['channels'].items():
            overwrites = None
            if ch_info['overwrites']:
                overwrites = {
                    roles_map.get(role): discord.PermissionOverwrite(**perms)
                    for role, perms in ch_info['overwrites'].items()
                    if role in roles_map
                }
            params = {
                "name": ch_name,
                "position": ch_info.get("position"),
                "overwrites": overwrites
            }
            if ch_info['category'] and ch_info['category'] in categories_map:
                params["category"] = categories_map[ch_info['category']]

            try:
                if ch_info['type'] == 'text':
                    await ctx.guild.create_text_channel(**params)
                elif ch_info['type'] == 'voice':
                    await ctx.guild.create_voice_channel(**params)
            except:
                pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def save(self, ctx, name: str):
        data = {
            "categories": await self.gather_categories(ctx),
            "channels": await self.gather_channels(ctx),
            "roles": await self.gather_roles(ctx)
        }
        os.makedirs("backups", exist_ok=True)
        with open(f"backups/{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        await ctx.send(f"Yedekleme başarılı: `{name}`")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, name: str):
        path = f"backups/{name}.json"
        if not os.path.isfile(path):
            await ctx.send("Böyle bir yedek bulunamadı.")
            return

        await self.clear_channels(ctx)
        await self.clear_roles(ctx)

        with open(path, "r", encoding="utf-8") as f:
            guild_data = json.load(f)

        roles_map = await self.recreate_roles(ctx, guild_data)
        await self.recreate_channels(ctx, guild_data, roles_map)
        await ctx.send(f"Yedek yüklendi: `{name}`")

async def setup(bot):
    await bot.add_cog(ServerClone(bot))
