import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import datetime
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

statuses = [
    'with fire',
    'with discord.py',
    'with Python',
    'a game',
]

async def change_status():
    await bot.wait_until_ready()

    while not bot.is_closed():
        for status in statuses:
            await bot.change_presence(activity=discord.Game(name=status))
            print(f"Status changed to {status}")
            await asyncio.sleep(60)

@bot.event
async def on_ready():
    print(f'The Bot is logged in as {bot.user}')
    print('Log:')
    await bot.change_presence(status=discord.Status.online)
    bot.loop.create_task(change_status())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: hi')

    await bot.process_commands(message)

@bot.command(name="help", description="Shows available commands")
async def help(ctx):
    embed = discord.Embed(
        title="Python Discord Bot",
        description="Commands:",
        color=0x00b0f4
    )
    embed.add_field(name="!help", value="Shows this help message", inline=False)
    embed.add_field(name="!github", value="Shows link to the bot's GitHub repository", inline=False)
    embed.add_field(name="!info", value="Shows information about the bot", inline=False)
    embed.add_field(name="!offline", value="Sets bot's status to offline", inline=False)
    embed.add_field(name="!online", value="Sets bot's status to online", inline=False)
    
    embed.set_author(
        name="Python Discord Bot",
        url="https://github.com/arbs09/python-discordbot"
    )
    
    await ctx.send(embed=embed)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !help')

@bot.command(name='info', description="Shows information about the bot")
async def info(ctx):
    await ctx.send('This is a discord bot, coded in Python!\nGitHub: https://github.com/arbs09/python-discordbot')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !info')

@bot.command(name='github', description="Shows link to the bot's GitHub repository")
async def github(ctx):
    await ctx.send('GitHub: https://github.com/arbs09/python-discordbot')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !github')

@bot.command(name='offline', description="Sets bot's status to offline")
async def offline(ctx):
    await bot.change_presence(status=discord.Status.offline)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !offline')

@bot.command(name='online', description="Sets bot's status to online")
async def online(ctx):
    await bot.change_presence(status=discord.Status.online)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !online')

bot.run(TOKEN)