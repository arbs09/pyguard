import os, discord, random, asyncio, re, requests, json
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URLHAUS_API_URL = 'https://urlhaus-api.abuse.ch/v1/url/'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

start_time = datetime.now()

def is_owner(ctx):
    return ctx.author.id == 706119023422603335

async def change_status():
    await bot.wait_until_ready()

    playing_statuses = [
        'with fire',
        'with discord.py',
        'with Python',
        'a game',
        'with linux',
    ]

    watching_statuses = [
        "Youtube",
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


url_pattern = re.compile(r'https?://[^\s]+')
checked_urls = set()

async def is_url_safe_urlhaus(url):
    global checked_urls
    
    if url in checked_urls:
        return True
    
    try:
        response = requests.post("https://urlhaus-api.abuse.ch/v1/url/", data={"url": url})
        response.raise_for_status()
        data = response.json()
        if data['query_status'] == 'ok':
            # URL is malicious
            checked_urls.add(url)  # Cache the result
            return False
        else:
            # URL is safe
            checked_urls.add(url)
            return True

    except requests.exceptions.RequestException as e:
        print(f"Error checking URL {url}: {e}")
    
    checked_urls.add(url)
    return True

@bot.event
async def on_ready():
    print(f'The Bot is logged in as {bot.user}')
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

    urls = url_pattern.findall(message.content)
    
    for url in urls:
        is_bad = await is_url_safe_urlhaus(url)
        if is_bad:
            try:
                await message.delete()
                print(f'{message.author} Postet a bad url')
                break
            except discord.Forbidden:
                print(f"Could not delete message due to permissions in channel: {message.channel.name}")
    
    
    await bot.process_commands(message)

@bot.command(name="help", description="Shows available commands")
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Python Discord Bot",
        description="Commands:",
        color=0x00b0f4
    )
    embed.add_field(name="!help", value="Shows this help message", inline=False)
    embed.add_field(name="!github", value="Shows link to the bot's GitHub repository", inline=False)
    embed.add_field(name="!info", value="Shows information about the bot", inline=False)
    embed.add_field(name="!getuserid", value="Shows your userid", inline=False)
    embed.add_field(name="!uptime", value="Shows the Uptime of the bot", inline=False)

    await ctx.send(embed=embed)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !help')

@bot.command(name='info', description="Shows information about the bot")
async def info(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Python Discord Bot Information",
        description="This is a discord bot, coded in Python!\nGitHub: https://github.com/arbs09/python-discordbot",
        color=0x00b0f4
    )
    await ctx.send(embed=embed)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !info')

@bot.command(name='github', description="Shows link to the bot's GitHub repository")
async def github(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="Python Discord Bot Github",
        description="GitHub: https://github.com/arbs09/python-discordbot",
        color=0x00b0f4
    )
    await ctx.send(embed=embed)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !github')

@bot.command()
async def uptime(ctx):
    await ctx.message.delete()
    
    current_time = datetime.now()
    uptime = current_time - start_time
    
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title="Python Discord Bot Uptime",
        description=f"{hours} hours, {minutes} minutes, {seconds} seconds",
        color=0x00b0f4
    )
    await ctx.send(embed=embed)


# games
## slot
symbols = ["🍇", "🍊", "🍐", "🍒", "🍋", "🍉", "🍀", "💸"]
weights = [20, 10, 10, 5, 10, 11, 15, 1]

def spin_slot_machine():
    return random.choices(symbols, weights=weights, k=3)

@bot.command(name='slots', help='Play the slot machine!')
async def slots(ctx):
    try:
        result = spin_slot_machine()

        if all(symbol == result[0] for symbol in result):
            message = "Jackpot! 🎉"
        elif result.count("🍒") == 3:
            message = "Triple cherries! 🍒🍒🍒"
        elif result.count("🍋") == 3:
            message = "Triple lemons! 🍋🍋🍋"
        elif result.count("🍀") == 3:
            message = "Good Luck 🍀🍀🍀"
        else:
            message = "Better luck next time!"

        embed = discord.Embed(title="Slot Machine", color=0xFFD700)
        embed.add_field(name="Result", value=f"{' '.join(result)}", inline=False)
        embed.add_field(name="Outcome", value=message, inline=False)

        message = await ctx.send(embed=embed)
        await message.add_reaction('🔄')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🔄' and reaction.message.id == message.id

        # Use the wait_for coroutine directly without unpacking into reaction, user
        await bot.wait_for('reaction_add', timeout=60.0, check=check)
        await message.delete()
        await slots(ctx)

    except Exception as e:
        await ctx.send(f"An error occurred: {type(e).__name__} - {e}")

# tools
@bot.command(name='getuserid', description="Get the ID of the user running the command")
async def get_user_id(ctx):
    user_id = ctx.author.id
    await ctx.message.delete()
    await ctx.send(f'Your user ID is: {user_id}')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !getuserid')

# Owner Commands
@bot.command(name='offline', description="Sets bot's status to offline")
async def offline(ctx):
    if not is_owner(ctx):
        await ctx.message.delete()
        return
    await ctx.message.delete()
    await bot.change_presence(status=discord.Status.offline)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !offline')

@bot.command(name='online', description="Sets bot's status to online")
async def online(ctx):
    if not is_owner(ctx):
        await ctx.message.delete()
        return
    await ctx.message.delete()
    await bot.change_presence(status=discord.Status.online)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !online')

@bot.command(name='changestatus', description="changes the status of the bot")
async def changestatus(ctx):
    if not is_owner(ctx):
        await ctx.message.delete()
        return
    await ctx.message.delete()
    await change_status()
    await ctx.send('Status manually changed!')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author} changed the random status.')

@bot.command(name='shutdown', description="Stops the Bot")
async def shutdown(ctx):
    if not is_owner(ctx):
        await ctx.message.delete()
        return
    await ctx.message.delete()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !shutdown')
    await bot.close()

bot.run(TOKEN)