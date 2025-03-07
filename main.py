import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import random

# custom imports
from utils import *
from uptime import get_uptime

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True

bot = discord.Bot(intents=intents)

async def change_status():
    await bot.wait_until_ready()
    while not bot.is_closed():
        statuses = json.loads(get_statuses())
        for type_, status_list in statuses.items():
            status = random.choice(status_list)
            if type_ == 'playing':
                await bot.change_presence(activity=discord.Game(name=status))
            elif type_ == 'watching':
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            elif type_ == 'listening':
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
            await asyncio.sleep(60)
        
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    for guild in bot.guilds:
        print(f'Connected to guild: {guild.name}')
        async for member in guild.fetch_members(limit=None):
            import_memers_from_server(member.id, member.name, guild.id)
    
    await bot.change_presence(status=discord.Status.online)
    bot.loop.create_task(change_status())

@bot.event
async def on_guild_join(guild):
    print(f'Joined new guild: {guild.name}')

    async for member in guild.fetch_members(limit=None):
        import_memers_from_server(member.id, member.name, guild.id)

@bot.event
async def on_member_join(member):
    import_memers_from_server(member.id, member.name, member.guild.id)
    
@bot.event
async def on_guild_update(before, after):
    if before.name != after.name:
        print(f'Guild {before.name} changed name to {after.name}')
    if before.owner != after.owner:
        print(f'Guild {before.name} changed owner from {before.owner} to {after.owner}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.author.bot:
        return

    give_global_xp(message.author, 10)
    give_server_xp(message.author, message.guild, 10)

    await bot.process_commands(message)

@bot.slash_command(name='help', description="Get help")
async def help(ctx: discord.ApplicationContext):
    embed = discord.Embed(title="Help", description="List of available commands", color=discord.Color.blue())
    embed.add_field(name="/clean_old", value="Clear the 100 oldest messages in a channel", inline=False)
    embed.add_field(name="/cleanup", value="Clear messages in a channel", inline=False)
    embed.add_field(name="/daten-export", value="Exportiere deine Daten", inline=False)
    embed.add_field(name="/get_global", value="Get your global level", inline=False)
    embed.add_field(name="/get_server", value="Get your server level", inline=False)
    embed.add_field(name="/getuserid", value="Get the ID of the user running the command", inline=False)
    embed.add_field(name="/help", value="Get help", inline=False)
    embed.add_field(name="/ping", value="Get bot latency", inline=False)
    embed.add_field(name="/uptime", value="Get bot uptime", inline=False)
    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name='invite', description="Join a new server")
async def invite(ctx: discord.ApplicationContext):
    await ctx.respond("You can invite me to your server using this link: https://pyguard.arbs09.dev/invite", ephemeral=True)

@bot.slash_command(name='ping', description="Get bot latency")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms', ephemeral=True)

@bot.slash_command(name='cleanup', description="Clear messages in a channel")
async def clear(ctx: discord.ApplicationContext, amount: int):
    if not ctx.author.guild_permissions.manage_messages and not is_owner(ctx):
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        return

    if amount > 100:
        await ctx.respond("You can only delete up to 100 messages at a time.", ephemeral=True)
        return

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.respond(f'Deleted {len(deleted)} messages.', ephemeral=True)

@bot.slash_command(name='clean_old', description="Clear the 100 oldest messages in a channel")
async def clean_old(ctx: discord.ApplicationContext):
    if not ctx.author.guild_permissions.manage_messages and not is_owner(ctx):
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        return

    messages = await ctx.channel.history(limit=100, oldest_first=True).flatten()
    if not messages:
        await ctx.respond("No messages found to delete.", ephemeral=True)
        return

    deleted = await ctx.channel.delete_messages(messages)
    if deleted is None:
        await ctx.respond("No messages were deleted.", ephemeral=True)
    else:
        await ctx.respond(f'Deleted {len(deleted)} messages.', ephemeral=True)

@bot.slash_command(name='uptime', description="Get bot uptime")
async def uptime(ctx: discord.ApplicationContext):
    await ctx.respond(f'Uptime: {get_uptime()}', ephemeral=True)

@bot.slash_command(name="daten-export", description="Exportiere deine Daten")
async def daten_export(ctx: discord.ApplicationContext):
    user = ctx.author

    embed = discord.Embed(
        title="Deine Daten",
        description="Deine Daten wurden dir per PM gesendet.",
        color=0x00b0f4
    )

    message = "Deine Daten welche wir über dein Discord Profil gespeichert haben:\n"

    await user.send(message + user_data_export(ctx))
    await ctx.respond(embed=embed, ephemeral=True)


@bot.slash_command(name='getuserid', description="Get the ID of the user running the command")
async def get_user_id(ctx: discord.ApplicationContext):
    user_id = ctx.author.id

    embed = discord.Embed(
        title="Your User ID:",
        description=f"{user_id}",
        color=0x00b0f4
    )

    await ctx.respond(embed=embed, ephemeral=True)

# xp

@bot.slash_command(name='get_global', description="Get your global level")
async def get_global_level(ctx: discord.ApplicationContext):
    user = ctx.author
    data = get_global(user)
    await ctx.respond(f'Deine globale XP: {data["xp"]}\nDein globales Level: {data["level"]}', ephemeral=True)

@bot.slash_command(name='get_server', description="Get your server level")
async def get_server_level(ctx: discord.ApplicationContext):
    user = ctx.author
    data = get_server(user, ctx.guild)
    await ctx.respond(f'Deine Server XP: {data["xp"]}\nDein Server Level: {data["level"]}', ephemeral=True)

bot.run(TOKEN)