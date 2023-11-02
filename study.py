from discord.ext import commands, tasks
import discord
import datetime
from dataclasses import dataclass
#For this file I had time to develop it and make it very easy for others to read it because I was working with a fellow student on it

BOT_TOKEN = "MTE0MzU4MzEzOTQ5OTg3NjQwMg.Gfj0R5.WDQiONWNWnckIEjck8GjWqGlVFl3D2LhN9CDaE" #This token does not work anymore due to the fact that others would be able to take control of my bot
CHANNEL_ID = 1143598078348251226
MAX_SESSION_TIME_MINUTES = 2

dataclass
class Session:
    is_active: bool = False
    start_time = int = 0

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
session = Session()




@bot.event
async def on_ready():
    print("Hello! Study bot is ready")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready")


@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count = 2)
async def break_reminder():
    if break_reminder.current_loop == 0:
        return
    
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes") 

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)
    
    await ctx.send(f"Result = {result}")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"New session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds = duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}.")


bot.run(BOT_TOKEN)
