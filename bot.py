import discord
import os
import random
import asyncio
import requests
import re
import json
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

# Initialize the bot's start time
start_time = datetime.now()

# Load environment variables
load_dotenv()

# Retrieve the bot token from the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True

# Initialize the bot
bot = discord.Bot(intents=intents)

# Load or create user_data.json
if os.path.exists('users.json'):
    with open('users.json', 'r') as f:
        user_data = json.load(f)
else:
    user_data = {}

# Save user_data to JSON file
def save_user_data():
    with open('users.json', 'w') as f:
        json.dump(user_data, f, indent=4)

# Define XP requirements for each level
xp_requirements = [20, 50, 100, 400, 1000, 1500]

# Function to add XP
def add_xp(user_id, author_name, xp, display_name, author_avatar, server_id, message_time=None):
    user_id = str(user_id)
    server_id = str(server_id)
    current_time = datetime.now().isoformat()
    
    if message_time is None:
        message_time = current_time
    else:
        # Ensure message_time is in correct format
        try:
            datetime.fromisoformat(message_time)
        except ValueError:
            message_time = current_time

    if user_id not in user_data:
        user_data[user_id] = {
            'xp': 0,
            'level': 1,
            'name': author_name,
            'avatar': str(author_avatar),
            'used_display_names': {server_id: [{
                'display_name': display_name,
                'first_seen': message_time,
                'last_seen': message_time
            }]},
            'first_login': message_time,
            'last_login': message_time
        }
    else:
        if 'first_login' not in user_data[user_id]:
            user_data[user_id]['first_login'] = message_time
        if 'last_login' not in user_data[user_id] or message_time > user_data[user_id]['last_login']:
            user_data[user_id]['last_login'] = message_time

        if server_id not in user_data[user_id]['used_display_names']:
            user_data[user_id]['used_display_names'][server_id] = []
        
        found = False
        for display_name_entry in user_data[user_id]['used_display_names'][server_id]:
            if display_name_entry['display_name'] == display_name:
                display_name_entry['last_seen'] = message_time
                found = True
                break
        
        if not found:
            user_data[user_id]['used_display_names'][server_id].append({
                'display_name': display_name,
                'first_seen': message_time,
                'last_seen': message_time
            })

    user_data[user_id]['xp'] += xp

    # Check for level up without resetting XP
    while user_data[user_id]['level'] <= len(xp_requirements) and user_data[user_id]['xp'] >= xp_requirements[user_data[user_id]['level'] - 1]:
        user_data[user_id]['level'] += 1

    user_data[user_id]['name'] = author_name
    user_data[user_id]['avatar'] = str(author_avatar)

    save_user_data() 

def is_owner(ctx):
    """Checks if the message author is the bot owner."""
    return ctx.author.id == 706119023422603335

async def change_status():
    """Changes the bot's status periodically."""
    await bot.wait_until_ready()

    playing_statuses = [
        'with fire',
        'with pycord',
        'with Python',
        'a game',
        'with Linux',
    ]

    watching_statuses = [
        "YouTube",
        "a Movie",
        "you",
    ]

    listening_statuses = [
        "Music",
        "a Podcast",
        "Radio",
        "Darknet Diaries"
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

    guilds_data = []

    print('Guilds:')
    for guild in bot.guilds:
        members_data = []
        async for member in guild.fetch_members(limit=None):
            member_data = {
                'id': member.id,
                'name': member.name,
                'is_bot': member.bot,
                'display_name': member.display_name,
                'top_role': member.top_role.id,
                'joined_at': member.joined_at.isoformat() if member.joined_at else None
            }
            members_data.append(member_data)

        guild_data = {
            'guild_id': guild.id,
            'guild_name': guild.name,
            'member_count': guild.member_count,
            'owner_id': guild.owner_id,
            'description': guild.description,
            'preferred_locale': guild.preferred_locale,
            'verification_level': str(guild.verification_level),
            'explicit_content_filter': str(guild.explicit_content_filter),
            'mfa_level': str(guild.mfa_level),
            'features': guild.features,
            'members': members_data
        }
        guilds_data.append(guild_data)
    
    with open('guilds.json', 'w') as f:
        json.dump(guilds_data, f, indent=4)

        print(f'- {guild.name} (ID: {guild.id})')
        print(f'    - Member count: {guild.member_count}')
    
    
    await bot.change_presence(status=discord.Status.online)
    bot.loop.create_task(change_status())

# add level counting
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    add_xp(message.author.id, message.author.name, 10, message.author.display_name, message.author.avatar, message.guild.id)

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
    embed.add_field(name="/modtools", value="Get a list of the tools for moderators of the bot", inline=False)
    embed.add_field(name="/github", value="Shows link to the bot's GitHub repository", inline=False)
    embed.add_field(name="/uptime", value="Shows the Uptime of the bot", inline=False)


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

    weeks, remainder = divmod(int(uptime.total_seconds()), 604800) 
    days, remainder = divmod(remainder, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title="Python Discord Bot Uptime",
        description=f"{weeks} weeks, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds",
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


@bot.slash_command(name="games", description="Get a list of the games of the bot")
async def games(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Python Discord Bot",
        description="Games:",
        color=0x00b0f4
    )

    embed.add_field(name="/slots", value="Play slots", inline=False)

    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name='slots', description="Shows link to the bot's GitHub repository")
async def slots(ctx: discord.ApplicationContext):

    embed = discord.Embed(
        title="Python Discord Bot Slots",
        description="This game is currently a work in progress",
        color=0x00b0f4
    )

    await ctx.respond(embed=embed, ephemeral=True)


@bot.slash_command(name="tools", description="Get a list of the tools of the bot")
async def tools(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Python Discord Bot",
        description="Tools:",
        color=0x00b0f4
    )

    embed.add_field(name="/getuserid", value="Get your discord user id", inline=False)
    embed.add_field(name="/getgloballevel", value="Check your global level and XP", inline=False)

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

@bot.slash_command(name="getgloballevel", description="Check your global level and XP")
async def getgloballevel(ctx: discord.ApplicationContext):
    user_id = str(ctx.author.id)

    noxpembed = discord.Embed(
        title="Python Discord Bot Global Level",
        description=f"{ctx.author.mention}, you have no XP yet.",
        color=0x00b0f4
    )
    
    if user_id in user_data:
        user_level = user_data[user_id]['level']
        user_xp = user_data[user_id]['xp']

        embed = discord.Embed(
            title="Python Discord Bot Global Level",
            description=f"{ctx.author.mention}, you are at level {user_level} with {user_xp} XP globally.",
            color=0x00b0f4
        )
        
        await ctx.respond(embed=embed, ephemeral=True)
    else:
        await ctx.respond(embed=noxpembed, ephemeral=True)



@bot.slash_command(name="modtools", description="Get a list of the tools for moderators of the bot")
async def games(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Python Discord Bot",
        description="Mod tools:",
        color=0x00b0f4
    )

    embed.add_field(name="/cleanup", value="Clear messages in a channel", inline=False)

    await ctx.respond(embed=embed, ephemeral=True)

@bot.slash_command(name='cleanup', description="Clear messages in a channel")
async def clear(ctx: discord.ApplicationContext, amount: int):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        return
    
    if amount > 100:
        await ctx.respond("You can only delete up to 100 messages at a time.", ephemeral=True)
        return

    deleted = await ctx.channel.purge(limit=amount)
    await ctx.respond(f'Deleted {len(deleted)} messages.', ephemeral=True)

bot.run(TOKEN)
