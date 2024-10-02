from datetime import datetime
import time
import os
import re
import subprocess
import asyncio
import platform

# auto install libraries if pip dont have them
try:
    import requests
    import discord
    from discord import app_commands
    from discord.ext import commands
    from discord.app_commands import checks
    from discord.utils import get
except ImportError:
    print("Libraries missing, installing...")
    os.system('python3 -m pip install -U requests')
    os.system('python3 -m pip install -U discord')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)

# bot variables
tracking = True
update_channel_id = None
notification_role = "@everyone"
update_frequency = 3
selected_games = ["Euro Truck Simulator 2", "American Truck Simulator"]

# versions
game_ets_version = "1.50.4.0s" # "1.50.4.0s" - current version
game_ats_version = "1.50.1.29s" # "1.50.1.29s" - current version

# from normal date to universal timestamp
timestamp = int(time.time())
discord_timestamp = f"<t:{timestamp}:F>"

def convert(value):
    return ":green_circle:" if value else ":red_circle:"

def ping():
    if platform.system().lower() == 'windows':
        result = subprocess.run(["ping", "api.truckersmp.com", "-n", "1", "-4"], stdout=subprocess.PIPE, text=True)
    else:
        result = subprocess.run(["ping", "api.truckersmp.com", "-c", "1", "-4"], stdout=subprocess.PIPE, text=True)
    match = re.search(r'time=(\d+\.\d+)', result.stdout)
    if match:
        return float(match.group(1))
    else:
        return "-"

# send message with webhook
async def send_update_message(title, description, game, version, footer_text):
    e = discord.Embed(title=title, description=description, color=0x969696)
    e.add_field(name="Game:", value=game)
    e.add_field(name="Version:", value=version, inline=False)
    e.add_field(name="Date:", value=f"{discord_timestamp}", inline=False)
    e.set_footer(text=footer_text)
    e.set_thumbnail(url="https://cdn.discordapp.com/attachments/1216748200283607130/1290009648010887178/refresh-ccw_1.png?ex=66fae69b&is=66f9951b&hm=0d4ae82ba194c1346d9fa7ecd1cabd5ee084192905575be414fc494203cf4c9a&")
    channel = bot.get_channel(update_channel_id)
    if channel:
        await channel.send(f"{notification_role}", embed=e)

async def get_version(ets_version=None, ats_version=None):
    global game_ets_version
    global game_ats_version
    site = requests.get("https://api.truckersmp.com/v2/version", timeout=update_frequency)
    if site.status_code == 200:
        data = site.json()
        if ets_version:
            supported_game_ets_version = data.get('supported_game_version')
            return supported_game_ets_version
        if ats_version:
            supported_game_ats_version = data.get('supported_ats_game_version')
            return supported_game_ats_version
    else:
        print(f"Failed to fetch data. Status code: {site.status_code}")

async def tracker():
    global game_ets_version, game_ats_version
    ets_version = await get_version(ets_version=True, ats_version=False)
    if game_ets_version != ets_version:
        previous_ets_version = game_ets_version
        game_ets_version = ets_version
        await send_update_message(
            "A new TruckersMP game supported version has been detected!",
            "New version has been released fully!",
            "Euro Truck Simulator 2",
            game_ets_version,
            "Tracker made by bdvzk."
        )
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   New ETS version detected: {game_ets_version}, Previous version: {previous_ets_version}")
    ats_version = await get_version(ets_version=False, ats_version=True)
    if game_ats_version != ats_version:
        previous_ats_version = game_ats_version
        game_ats_version = ats_version
        await send_update_message(
            "A new TruckersMP game supported version has been detected!",
            "New version has been released fully!",
            "American Truck Simulator",
            game_ats_version,
            "Tracker made by bdvzk."
        )
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   New ATS version detected: {game_ats_version}, Previous version: {previous_ats_version}")

# loop for checking versions
async def track_versions():
    while True:
        if tracking:
            await tracker()
            await asyncio.sleep(update_frequency)
        else:
            await asyncio.sleep(1)

# discord bot commands below
@bot.hybrid_command(description="Change the channel to notify you of a new supported TMP version.")
@checks.has_permissions(administrator=True)
async def manage_channel(ctx, channel_id: str):
    global update_channel_id
    try:
        channel_id_int = int(channel_id)
        if update_channel_id == channel_id_int:
            await ctx.interaction.response.send_message(f"This channel has already been selected!", ephemeral=True)
        else:
            update_channel_id = channel_id_int
            await ctx.interaction.response.send_message(f":white_check_mark: Updates channel successfully changed to <#{channel_id_int}> !", ephemeral=True)
    except ValueError:
        await ctx.interaction.response.send_message("Please input a valid channel ID!", ephemeral=True)

@bot.hybrid_command(description="Set the games to monitor.")
@checks.has_permissions(administrator=True)
async def set_games(ctx, *, games: str):
    global selected_games
    selected_games = [game.strip() for game in games.split(",")]
    await ctx.interaction.response.send_message(
        f":white_check_mark: Selected games successfully changed to: {', '.join(selected_games)}!", ephemeral=True)

@bot.hybrid_command(description="Change the role for update notifications.")
@checks.has_permissions(administrator=True)
async def set_role(ctx, *, role: str):
    global notification_role
    notification_role = role
    await ctx.interaction.response.send_message(f":white_check_mark: Notification role successfully changed to: {notification_role}!", ephemeral=True)

@bot.hybrid_command(description="Change the request delay.")
@checks.has_permissions(administrator=True)
async def set_frequency(ctx, frequency: int):
    global update_frequency
    if update_frequency == frequency:
        await ctx.interaction.response.send_message(f"This request delay has already been selected!", ephemeral=True)
    else:
        update_frequency = frequency
        await ctx.interaction.response.send_message(f":white_check_mark: Request delay successfully changed to {update_frequency} second(s)!", ephemeral=True)

@bot.hybrid_command(description="Turn the tracker on or off.")
@checks.has_permissions(administrator=True)
async def toggle(ctx, value: bool):
    global tracking
    if value == tracking:
        await ctx.interaction.response.send_message(f"Tracker's already {'on' if tracking else 'off'}.", ephemeral=True)
    else:
        tracking = value
        await ctx.interaction.response.send_message(
            f"The tracker has been turned **{'on' if tracking else 'off'}**.", ephemeral=True)

@bot.hybrid_command(description="Shows all information from the tracker.")
@checks.has_permissions(administrator=True)
async def info(ctx):
    global tracking
    global update_channel_id
    global update_frequency
    global selected_games
    global notification_role
    e = discord.Embed(title="TruckersMP tracker information", description=f"Tracker's state: {convert(tracking)}", color=0x969696)
    e.add_field(name=f"Latest Supported Versions:", value=f"Euro Truck Simulator 2: `{await get_version(ets_version=True, ats_version=False)}`\nAmerican Truck Simulator: `{await get_version(ets_version=False, ats_version=True)}`")
    e.add_field(name=f"Selected Channel:", value=f"<#{update_channel_id}>", inline=False)
    e.add_field(name=f"Selected Role:", value=f"{notification_role}", inline=False)
    e.add_field(name="Selected Game(s):", value=f"{', '.join(selected_games)}", inline=False)
    e.add_field(name="Request Delay:", value=f"{update_frequency} seconds.", inline=False)
    e.add_field(name="Request Latency:", value=f"{ping()}ms", inline=False)
    e.set_footer(text="Tracker made by bdvzk")
    e.set_thumbnail(url="https://cdn.discordapp.com/attachments/676467713555562538/1290713604781379584/chart-pie_1.png?ex=66fd7637&is=66fc24b7&hm=92216b690941c15d5c644c1dbcc295271b170e259815bdb817569215678e6615&")
    await ctx.interaction.response.send_message(embed=e, ephemeral=True)

@bot.hybrid_command(description="The latest current supported versions.")
async def tmp_version(ctx):
    await ctx.interaction.response.send_message(f"Euro Truck Simulator 2: `{await get_version(ets_version=True, ats_version=False)}`\nAmerican Truck Simulator: `{await get_version(ets_version=False, ats_version=True)}`", ephemeral=False)

#@bot.hybrid_command(description="Change the latest update of ets2.")
#async def change_version(ctx, version: int):
#    global game_ets_version
#    game_ets_version = version

@bot.event
async def on_ready():
    print(f'Started. Bot: {bot.user}')
    await bot.tree.sync()
    await track_versions()

# fix for an error when a user sends a command name without slash
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

bot.run('token')
