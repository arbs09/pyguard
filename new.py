import discord
import os
import random
import asyncio
import requests
import re
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

# Initialize the bot's start time
start_time = datetime.now()

# Load environment variables
load_dotenv()

# Retrieve the bot token from the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize the bot
bot = discord.Bot()

def is_owner(ctx):
    """Checks if the message author is the bot owner."""
    return ctx.author.id == 706119023422603335

async def change_status():
    """Changes the bot's status periodically."""
    await bot.wait_until_ready()

    playing_statuses = [
        'with fire',
        'with discord.py',
        'with Python',
        'a game',
        'with Linux',
    ]

    watching_statuses = [
        "YouTube",
        "a Movie",
    ]

    listening_statuses = [
        "to Music",
        "to a Podcast",
        "to Radio",
        "to Darknet Diaries"
    ]

    while not bot.is_closed():
        activity_type = random.choice(["playing", "watching", "listening"])

        if activity_type == "playing":
            status = random.choice(playing_statuses)
            activity = discord.Game(name=status)
        elif activity_type == "watching":
            status = random.choice(watching_statuses)
            activity = discord.Activity(type=discord.ActivityType.watching, name=status)
        elif activity_type == "listening":
            status = random.choice(listening_statuses)
            activity = discord.Activity(type=discord.ActivityType.listening, name=status)

        await bot.change_presence(activity=activity)
        print(f"Status changed to {activity_type} {status}")
        await asyncio.sleep(300)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(status=discord.Status.online)
    bot.loop.create_task(change_status())


@bot.slash_command(name="help", description="Get help from the Bot")
async def help(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Python Discord Bot",
        description="Commands:",
        color=0x00b0f4
    )
    embed.add_field(name="/help", value="Shows this message", inline=False)
    embed.add_field(name="/tools", value="Get a list of the tools of the bot", inline=False)
    embed.add_field(name="/games", value="Get a list of the games of the bot", inline=False)
    embed.add_field(name="/github", value="Shows link to the bot's GitHub repository", inline=False)
    embed.add_field(name="/uptime", value="Shows the Uptime of the bot", inline=False)

    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="tools", description="Get a list of the tools of the bot")
async def tools(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Python Discord Bot",
        description="Tools:",
        color=0x00b0f4
    )

    embed.add_field(name="/getuserid", value="Get your discord user id", inline=False)

    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="games", description="Get a list of the games of the bot")
async def games(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Python Discord Bot",
        description="Games:",
        color=0x00b0f4
    )

    embed.add_field(name="/slots", value="Play slots", inline=False)

    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name='github', description="Shows link to the bot's GitHub repository")
async def github(ctx: discord.ApplicationContext):

    embed = discord.Embed(
        title="Python Discord Bot Github",
        description="This is a discord bot, coded in Python!\nGitHub: https://github.com/arbs09/python-discordbot",
        color=0x00b0f4
    )

    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name="uptime", description="Check the bot's uptime")
async def uptime(ctx: discord.ApplicationContext):
    current_time = datetime.now()
    uptime = current_time - start_time

    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title="Python Discord Bot Uptime",
        description=f"{hours} hours, {minutes} minutes, {seconds} seconds",
        color=0x00b0f4
    )
    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name='changestatus', description="changes the status of the bot")
async def changestatus(ctx: discord.ApplicationContext):
    if not is_owner(ctx):
        return
    
    embed = discord.Embed(
        title="Python Discord Bot Status Change",
        description="Status manually changed!",
        color=0x00b0f4
    )
    
    await ctx.respond(embed=embed, ephemeral=True)
    await change_status()

@bot.slash_command(name='getuserid', description="Get the ID of the user running the command")
async def get_user_id(ctx: discord.ApplicationContext):
    user_id = ctx.author.id

    embed = discord.Embed(
        title="Python Discord Bot Status Change",
        description=f"Your user ID is: {user_id}",
        color=0x00b0f4
    )

    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name='slots', description="Shows link to the bot's GitHub repository")
async def slots(ctx: discord.ApplicationContext):

    embed = discord.Embed(
        title="Python Discord Bot Slots",
        description="This game is currently a work in progress",
        color=0x00b0f4
    )

    await ctx.respond(embed=embed, ephemeral=True)


bot.run(TOKEN)
