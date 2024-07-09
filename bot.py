import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'The Bot is logged in as {bot.user}')
    print('Log:')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('a game'))
    await bot.tree.sync()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: hi')

    await bot.process_commands(message)

@bot.tree.command(name="help", description="help")
async def help(ctx):
    embed = discord.Embed(
                      description="```\n!help   | You are here\n!Github | Shows Link to the Bots Github\n!info   | Shows Information about the Bot\n```",
                      colour=0x00b0f4)

    embed.set_author(name="Python Discord Bot",
                 url="https://github.com/arbs09/python-discordbot")

    await ctx.send(embed=embed)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !help')

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

@bot.command(name='offline')
async def offline(ctx):
    await bot.change_presence(status=discord.Status.offline)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !offline')

@bot.command(name='online')
async def online(ctx):
    await bot.change_presence(status=discord.Status.online)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !online')

@bot.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !echo {arg}')


bot.run(TOKEN)