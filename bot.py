import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'The Bot is logged in as {bot.user}')

    if len(bot.guilds) != 1:
        print('Bot is not in exactly one guild. Exiting...')
        await bot.close()
        return

    guild = bot.get_guild(GUILD_ID)
    print(f'Connected to guild: {guild.name} (ID: {guild.id})')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: hi')

    await bot.process_commands(message)

@bot.command(name='info')
async def info(ctx):
    await ctx.send('This is a discord bot, coded in python!\nGithub: https://github.com/arbs09/python-discordbot')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !info')

@bot.command(name='github')
async def github(ctx):
    await ctx.send('Github: https://github.com/arbs09/python-discordbot')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !github')

@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)

bot.run(TOKEN)
