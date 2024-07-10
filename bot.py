import os, discord, random, asyncio, re, requests, json
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
URLHAUS_API_URL = 'https://urlhaus-api.abuse.ch/v1/url/'

domains_url = 'https://raw.githubusercontent.com/arbs09/python-discordbot/main/blacklist/domains.txt'
phrases_url = 'https://raw.githubusercontent.com/arbs09/python-discordbot/main/blacklist/phrases.txt'

def fetch_list(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Failed to fetch data from {url}")
        return []

blacklisted_domains = fetch_list(domains_url)
print("updated Blacklisted Domains")

blacklisted_phrases = fetch_list(phrases_url)
print("updated Blacklisted Phrases")


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

locked_channels = []

start_time = datetime.now()

try:
    with open('locked_channels.json', 'r') as f:
        locked_channels = json.load(f)
except FileNotFoundError:
    locked_channels = []

def is_owner(ctx):
    return ctx.author.id == 706119023422603335

def save_locked_channels():
    with open('locked_channels.json', 'w') as f:
        json.dump(locked_channels, f)

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


    if message.channel.id in locked_channels and not message.content.startswith('!unlock'):
        await message.delete()
        return

    urls = url_pattern.findall(message.content)
    
    for url in urls:
        is_bad = await is_url_safe_urlhaus(url)
        if is_bad:
            try:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                await message.delete()
                print(f'{timestamp}: {message.author} Postet a bad url (urlhaus)')
                break
            except discord.Forbidden:
                print(f"{timestamp}: Could not delete message due to permissions in channel: {message.channel.name}")
    
    for domain in blacklisted_domains:
        if domain in message.content:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await message.delete()
            print(f'{timestamp}: {message.author} Postet a bad url (blacklistet domains)')
            return
    
    for phrase in blacklisted_phrases:
        if phrase in message.content:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await message.delete()
            print(f'{timestamp}: {message.author} Postet a bad message (blacklistet phrases)')
            return
    
    if message.content.startswith('hi'):
        await message.channel.send('Hello!')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} - {message.author}: hi')
    
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

    await ctx.send(embed=embed, delete_after=120)
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
    await ctx.send(embed=embed, delete_after=60)
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
    await ctx.send(embed=embed, delete_after=60)
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
    await ctx.send(embed=embed, delete_after=60)


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
            message = "x3 👏👏👏"
        elif result.count("🍒") == 3:
            message = "Triple cherries! 🍒🍒🍒"
        elif result.count("🍋") == 3:
            message = "Triple lemons! 🍋🍋🍋"
        elif result.count("🍀") == 3:
            message = "Good Luck 🍀🍀🍀"
        elif result.count("💸") == 3:
            message = "🎉🎉🎉 Jackpot! 🎉🎉🎉"
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'{timestamp}: 🎉🎉🎉 {ctx.author} hit a Jackpot! 🎉🎉🎉')
        else:
            message = "Better luck next time!"

        embed = discord.Embed(title="Slot Machine", color=0xFFD700)
        embed.add_field(name="Result", value=f"{' '.join(result)}", inline=False)
        embed.add_field(name="Outcome", value=message, inline=False)

        message = await ctx.send(embed=embed)
        await message.add_reaction('🔄')

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '🔄' and reaction.message.id == message.id

        await bot.wait_for('reaction_add', timeout=60.0, check=check)
        await message.delete()
        await slots(ctx)

    except Exception as e:
        await message.delete()
        await ctx.message.delete()

# tools
@bot.command(name='getuserid', description="Get the ID of the user running the command")
async def get_user_id(ctx):
    user_id = ctx.author.id
    await ctx.message.delete()
    await ctx.send(f'Your user ID is: {user_id}', delete_after=60)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} - {ctx.author}: !getuserid')

# Owner Commands
@bot.command(name='clearall', description="Clear all messages in a chat")
async def clearall(ctx):
    if not is_owner(ctx):
        await ctx.message.delete()
        return
     
    await ctx.message.delete()
    await ctx.send("Clearing all messages...", delete_after=2)
    
    def check_msg(msg):
        return True
    
    while True:
        deleted = await ctx.channel.purge(limit=100, check=check_msg)
        if len(deleted) < 100:
            break
    
    await ctx.send("All messages have been cleared!", delete_after=10)

@bot.command()
async def lock(ctx):
    if not is_owner(ctx):
        await ctx.message.delete()
        return
    await ctx.message.delete()
    if ctx.channel.id not in locked_channels:
        locked_channels.append(ctx.channel.id)
        save_locked_channels()
        await ctx.send(f'{ctx.channel.mention} is now locked.')
    else:
        await ctx.send(f'{ctx.channel.mention} is already locked.', delete_after=10)

@bot.command()
async def unlock(ctx):
    if not is_owner(ctx):
        await ctx.message.delete()
        return
    await ctx.message.delete()
    if ctx.channel.id in locked_channels:
        locked_channels.remove(ctx.channel.id)
        save_locked_channels()
        await ctx.send(f'{ctx.channel.mention} is now unlocked.', delete_after=600)
    else:
        await ctx.send(f'{ctx.channel.mention} is not locked., delete_after=10')

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