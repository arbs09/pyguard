import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'The Bot is logged in as {bot.user}')
    print('Log:')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: hi')

    elif message.content.startswith('!info'):
        await message.channel.send('This is a discord bot, coded in python!\nGithub: https://github.com/arbs09/python-discordbot')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: !info')

    elif message.content.startswith('!github'):
        await message.channel.send('Github: https://github.com/arbs09/python-discordbot')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: !github')

    await bot.process_commands(message)

@bot.command()
async def test(ctx, *, arg):
    await ctx.send(arg)

bot.run(TOKEN)
