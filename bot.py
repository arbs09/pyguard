import os

import discord
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print('The Bot is logged in as {0.user}'.format(client))

    print('Log:')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
 
    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: hi')
    
     
    if message.content.startswith('!info'):
        await message.channel.send('This is a discord bot, coded in python!\nGithub: https://github.com/arbs09/python-discordbot')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: !info')

    if message.content.startswith('!github'):
        await message.channel.send('Github: https://github.com/arbs09/python-discordbot')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: !github')

client.run(TOKEN)